#!/usr/bin/env python
# coding=utf-8

import re
import os.path

from ..common import script_utils


class tokenizer():
    def __init__(self, lang=None, split_sentence=False):
        self.split_sentence = split_sentence

        # nonbreaking prefixes
        self.nbr_prefixes = dict()

        if lang:
            self.set_lang(lang)
        else:
            self.lang = None
            self.script = None

        # precompile regexes
        self.precompile()

    def set_lang(self, lang):
        self.lang = lang
        self.script, self.script_info = script_utils.get_primary_script(lang)

        self.load_prefixes([self.script, self.lang])

    def load_prefixes(self, lists):
        # Always load latn and eng
        lists.extend(['latn', 'eng'])

        # Get unique list of files to be loaded
        lists = list(set(lists))

        file_path = os.path.dirname(__file__)
        for ext in lists:
            filepath = '%s/data/nbr_prefixes.%s' % (file_path, ext)

            # Ignore if file is not present
            if not os.path.isfile(filepath):
                continue

            with open(filepath) as fp:
                for l in fp:
                    line = l.decode('utf-8')
                    if line.startswith('#'):
                        continue
                    if '#NUMERIC_ONLY#' in line:
                        prefix = line.replace('#NUMERIC_ONLY#', '').strip()
                        self.nbr_prefixes[prefix] = 2
                    else:
                        self.nbr_prefixes[line.strip()] = 1

    def precompile(self):
        # remove junk characters
        self.junk = re.compile('[\x00-\x1f]')
        # seperate out on Latin-1 supplementary characters
        self.latin = re.compile(u'([\xa1-\xbf\xd7\xf7])')
        # seperate out on general unicode punctituations except "’"
        self.upunct = re.compile(u'([\u2012-\u2018\u201a-\u206f])')
        # seperate out on unicode mathematical operators
        self.umathop = re.compile(u'([\u2200-\u2211\u2213-\u22ff])')
        # seperate out on unicode fractions
        self.ufrac = re.compile(u'([\u2150-\u2160])')
        # seperate out on unicode superscripts and subscripts
        self.usupsub = re.compile(u'([\u2070-\u209f])')
        # seperate out on unicode currency symbols
        self.ucurrency = re.compile(u'([\u20a0-\u20cf])')
        # seperate out all "other" ASCII special characters
        self.specascii = re.compile(r'([\\!@#$%^&*()+={\[}\]|";:<>?`~/])')

        # Email and URLs
        self.email = re.compile(r'[a-zA-Z.+]+@[a-zA-Z]+(?:\.[a-zA-Z]+)+')
        self.url = re.compile(r'(?:https?://|ftps?://|file://|www.)[^ ,\]>]+')

        # keep multiple dots together
        self.multidot = re.compile(r'(\.\.+)')

        # keep multiple purna-viram together
        self.multiviram = re.compile(u'(\u0964\u0964+)')
        # keep multiple purna deergh-viram together
        self.multidviram = re.compile(u'(\u0965\u0965+)')

        # split contractions right (both "'" and "’")
        self.numcs = re.compile(u"([0-9\u0966-\u096f])(['\u2019\u02bc])s")
        self.aca = re.compile(
            u"([a-zA-Z\u0080-\u024f])(['\u2019\u02bc])([a-zA-Z\u0080-\u024f])"
        )
        self.acna = re.compile(
            u"([a-zA-Z\u0080-\u024f])(['\u2019\u02bc])([^a-zA-Z\u0080-\u024f])"
        )
        self.nacna = re.compile(
            u"([^a-zA-Z\u0080-\u024f])(['\u2019\u02bc])" +
            u"([^a-zA-Z\u0080-\u024f])"
        )
        self.naca = re.compile(
            u"([^a-zA-Z0-9\u0966-\u096f\u0080-\u024f])" +
            u"(['\u2019\u02bc])([a-zA-Z\u0080-\u024f])"
        )

        # multiple hyphens
        self.multihyphen = re.compile('(-+)')
        # restore multi-dots
        self.restoredots = re.compile(r'__(DOT)(\1*)MULTI__')
        self.restoreviram = re.compile(r'__(PNVM)(\1*)MULTI__')
        self.restoredviram = re.compile(r'__(DGVM)(\1*)MULTI__')

        self.splitsenir1 = re.compile(
            u' ([|.!?\u0964\u0965]) ([\u0900-\u0d7f\u201c\u2018A-Z])'
        )
        self.splitsenir2 = re.compile(
            u' ([|.!?\u0964\u0965]) ([\)\}\]\'"\u2019\u201d> ]+) '
        )

    def normalize(self, text):
        """
        Performs some common normalization, which includes:
            - Byte order mark, word joiner, etc. removal
            - ZERO_WIDTH_NON_JOINER and ZERO_WIDTH_JOINER removal
            - ZERO_WIDTH_SPACE, NO_BREAK_SPACE, NEW_LINE replaced by spaces
        """
        text = text.replace(u'\uFEFF', '')     # BYTE_ORDER_MARK
        text = text.replace(u'\uFFFE', '')     # BYTE_ORDER_MARK_2
        text = text.replace(u'\u2060', '')     # WORD_JOINER
        text = text.replace(u'\u00AD', '')     # SOFT_HYPHEN
        text = text.replace(u'\u200D', '')     # ZERO_WIDTH_JOINER
        text = text.replace(u'\u200C', '')     # ZERO_WIDTH_NON_JOINER
        text = text.replace(u'\u200B', ' ')    # ZERO_WIDTH_SPACE
        text = text.replace(u'\u00A0', ' ')    # NO_BREAK_SPACE
        text = text.replace(u'\n', ' ')        # NEW_LINE

        return text

    def tokenize(self, text):
        if not self.lang:
            # Detect script and guess language
            self.set_lang(script_utils.guess_language(text))

        # text = text.decode('utf-8', errors='ignore')
        text = self.normalize(text)
        text = ' %s ' % (text)
        # remove junk characters
        text = self.junk.sub('', text)
        # seperate out on Latin-1 supplementary characters
        text = self.latin.sub(r' \1 ', text)
        # seperate out on general unicode punctituations except "’"
        text = self.upunct.sub(r' \1 ', text)
        # seperate out on unicode mathematical operators
        text = self.umathop.sub(r' \1 ', text)
        # seperate out on unicode fractions
        text = self.ufrac.sub(r' \1 ', text)
        # seperate out on unicode superscripts and subscripts
        text = self.usupsub.sub(r' \1 ', text)
        # seperate out on unicode currency symbols
        text = self.ucurrency.sub(r' \1 ', text)
        # seperate out on "_" so that we can use that for special sequances
        text = text.replace('_', ' _ ')

        # Handle emails and URLs
        self.emails = self.email.findall(text)
        self.urls = self.url.findall(text)
        for i, email in enumerate(self.emails):
            text = text.replace(email, "__EMAIL%d__" % i)
        for i, url in enumerate(self.urls):
            text = text.replace(url, "__URL%d__" % i)

        # seperate out all "other" ASCII special characters
        text = self.specascii.sub(r' \1 ', text)

        # TODO: Handle conversion between VISARGA and :

        # keep multiple dots together
        text = self.multidot.sub(
            lambda m: r' __%sMULTI__ ' % ('DOT' * len(m.group(1))),
            text
        )

        # keep multiple purna-viram together
        text = self.multiviram.sub(
            lambda m: r' __%sMULTI__ ' % ('PNVM' * len(m.group(1))),
            text
        )
        # keep multiple purna deergh-viram together
        text = self.multidviram.sub(
            lambda m: r' __%sMULTI__ ' % ('DGVM' * len(m.group(1))),
            text
        )

        # split contractions right (both "'" and "’")
        text = self.nacna.sub(r"\1 \2 \3", text)
        text = self.naca.sub(r"\1 \2 \3", text)
        text = self.acna.sub(r"\1 \2 \3", text)
        text = self.aca.sub(r"\1 \2\3", text)
        text = self.numcs.sub(r"\1 \2s", text)
        text = text.replace("''", " ' ' ")

        # handle non-breaking prefixes
        words = text.split()
        text_len = len(words) - 1
        text = str()
        for i, word in enumerate(words):
            if word.endswith('.'):
                dotless = word[:-1]
                if dotless.isdigit():
                    word = dotless + ' .'
                elif ('.' in dotless) or \
                        self.nbr_prefixes.get(dotless, 0) == 1 or \
                        (i < text_len and words[i+1][0].islower()):
                    pass
                elif self.nbr_prefixes.get(dotless, 0) == 2 and \
                        (i < text_len and words[i+1][0].isdigit()):
                    pass
                else:
                    word = dotless + ' .'
            text += "%s " % word

        # seperate out "," except for digits in respective script
        text = re.sub(
            u'([^{digits}]),'.format(
                digits=self.script_info.get_digits()
            ),
            r'\1 , ',
            text
        )
        text = re.sub(
            u',([^{digits}])'.format(
                digits=self.script_info.get_digits()
            ),
            r' , \1',
            text
        )

        # separate out on characters followed by foreign characters
        # deergh viram and vice-versa
        text = re.sub(
            u'([{nd}])([^{nd}\u2212\.-]|[\u0964-\u0965])'.format(
                nd=self.script_info.get_nondigits()
            ),
            r'\1 \2',
            text
        )
        text = re.sub(
            u'([^{nd}\u2212\.-]|[\u0964-\u0965])([{nd}])'.format(
                nd=self.script_info.get_nondigits()
            ),
            r'\1 \2',
            text
        )

        # Seperate out special characters and symbols
        if self.script_info.get_specials():
            text = re.sub(
                u'({specials})'.format(
                    specials=self.script_info.get_specials()
                ),
                r' \1 ',
                text
            )

        # seperate out hyphens
        text = self.multihyphen.sub(
            lambda m: r'%s' % (' '.join('-' * len(m.group(1)))),
            text
        )
        text = re.sub(
            u'(-?[{digits}]-+[{digits}]-?){{,}}'.format(
                digits=self.script_info.get_digits()
            ),
            lambda m: r'%s' % (m.group().replace('-', ' - ')),
            text
        )

        text = text.split()
        text = ' '.join(text)

        # restore multiple dots, purna virams and deergh virams
        text = self.restoredots.sub(
            lambda m: r'.%s' % ('.' * (len(m.group(2)) / 3)),
            text
        )
        text = self.restoreviram.sub(
            lambda m: u'\u0964%s' % (u'\u0964' * (len(m.group(2)) / 4)),
            text
        )
        text = self.restoredviram.sub(
            lambda m: u'\u0965%s' % (u'\u0965' * (len(m.group(2)) / 4)),
            text
        )

        # restore emails and urls
        for i, email in enumerate(self.emails):
            text = text.replace("__EMAIL%d__" % i, email)
        for i, url in enumerate(self.urls):
            text = text.replace("__URL%d__" % i, url)

        # split sentences
        if self.split_sentence:
            text = self.splitsenir1.sub(r' \1\n\2', text)
            text = self.splitsenir2.sub(r' \1 \2\n', text)

        return map(lambda x: x.split(), text.split(u'\n'))
