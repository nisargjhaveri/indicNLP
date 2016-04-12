#!/usr/bin/env python
# coding=utf-8

scripts_info = {
    'deva': {
        'name': 'Devanagari',
        'languages': ['hin', 'mar', 'nep', 'bod', 'kok'],
        'range': ur'\u0900-\u097f',
        'digits': ur'\u0966-\u096f',
        'specials': ur''
    },
    'beng': {
        'name': 'Bengali',
        'languages': ['ben', 'asm'],
        'range': ur'\u0980-\u09ff',
        'digits': ur'\u09e6-\u09ef',
        # currency signs, BENGALI ISSHAR
        'specials': ur'\u09f2\u09f3\u09fa\u09fb',
    },
    'guru': {
        'name': 'Gurmukhi',
        'languages': ['pan'],
        'range': ur'\u0a00-\u0a7f',
        'digits': ur'\u0a66-\u0a6f',
        'specials': ur''
    },
    'gujr': {
        'name': 'Gujarati',
        'languages': ['guj'],
        'range': ur'\u0a80-\u0aff',
        'digits': ur'\u0ae6-\u0aef',
        # currency signs, GUJARATI OM
        'specials': ur'\u0AD0\u0AF1'
    },
    'orya': {
        'name': 'Oriya',
        'languages': ['ori'],
        'range': ur'\u0b00-\u0b7f',
        'digits': ur'\u0b66-\u0b6f',
        # Oriya fraction symbols
        'specials': ur'\u0B72-\u0B77'
    },
    'taml': {
        'name': 'Tamil',
        'languages': ['tam'],
        'range': ur'\u0b80-\u0bff',
        'digits': ur'\u0be6-\u0bef',
        # calendrical, clerical, currency signs etc.
        'specials': ur'\u0bd0\u0bf3-\u0bff'
    },
    'telu': {
        'name': 'Telugu',
        'languages': ['tel'],
        'range': ur'\u0c00-\u0c7f',
        'digits': ur'\u0c66-\u0c6f',
        # Telugu fractions and weights
        'specials': ur'\u0c78-\u0c7f'
    },
    'knda': {
        'name': 'Kannada',
        'languages': ['kan'],
        'range': ur'\u0c80-\u0cff',
        'digits': ur'\u0ce6-\u0cef',
        'specials': ur''
    },
    'mlym': {
        'name': 'Malayalam',
        'languages': ['mal'],
        'range': ur'\u0d00-\u0d7f',
        'digits': ur'\u0d66-\u0d72',
        # Malayalam fraction symbols
        'specials': ur'\u0d73\u0d74\u0d75'
    },
}


class Script:
    def __init__(self, script, script_info):
        self.iso_code = script
        self.script_info = script_info

    def get_code(self):
        return self.iso_code

    def get_name(self):
        return self.script_info['name']

    def get_languages(self):
        return self.script_info['languages']

    def get_digits(self):
        return u'0-9{digits}'.format(digits=self.script_info['digits'])

    def get_nondigits(self):
        block = self.script_info['range']
        digits = self.script_info['digits']

        return block[0] + u'-' + unichr(ord(digits[0]) - 1) + \
            unichr(ord(digits[-1]) + 1) + u'-' + block[-1]

    def get_range(self):
        return self.script_info['range']

    def get_specials(self):
        return self.script_info['specials']


def get_primary_script(lang):
    for script in scripts_info:
        if lang in scripts_info[script]['languages']:
            return script, Script(script, scripts_info[script])


def identify_script(text):
    scripts = []
    for script in scripts_info:
        scripts.append([
            0,
            script,
            ord(scripts_info[script]['range'][0]),
            ord(scripts_info[script]['range'][-1])
        ])

    limit = 15
    hard_limit = 100
    for char in text:
        for script in scripts:
            in_script = 1 if script[2] <= ord(char) <= script[3] else 0
            script[0] += in_script
            limit -= in_script

        hard_limit -= 1
        if not limit or not hard_limit:
            break

    scripts.sort(key=lambda s: s[0], reverse=True)
    if scripts[0][0]:
        return scripts[0][1]
    else:
        raise Exception("Could not identify script")


def guess_language(text):
    script = identify_script(text)
    lang = scripts_info[script]['languages'][0]
    return lang
