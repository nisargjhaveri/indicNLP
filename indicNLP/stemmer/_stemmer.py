#!/usr/bin/env python
# coding=utf-8

import os.path


class stemmer:
    def __init__(self, lang, model):
        self.lang = lang
        self.model = model
        self.min_stem_size = 1  # int(length) or 'half'

        self._load_suffix_list()

    def _load_suffix_list(self):
        suffixes = []

        listfile = self._get_list_file()
        for line in listfile:
            # Ignore everything after #
            line = line.decode('utf-8').split('#')[0]

            suffix = line.strip()
            if not suffix:
                continue
            suffixes.append(suffix)

        # Sort suffixes by length, lingest first
        suffixes.sort(key=lambda x: len(x), reverse=True)

        self.suffixes = suffixes

    def _get_list_file(self, mode='r'):
        filename = '%s_suffixes_%s.list' % (self.lang, self.model)
        filepath = os.path.join(os.path.dirname(__file__), 'data', filename)
        return open(filepath, mode)

    def stem_word(self, word):
        for suffix in self.suffixes:
            if word.endswith(suffix):
                stem = word[:-len(suffix)]
                if self.min_stem_size == 'half' and len(stem) < len(word) / 2:
                    continue
                elif len(stem) < self.min_stem_size:
                    continue
                return stem

        return word

    def stem(self, sentences):
        stemmed_sentences = []
        for sent in sentences:
            stemmed_sentences.append(
                map(self.stem_word, sent)
            )

        return stemmed_sentences
