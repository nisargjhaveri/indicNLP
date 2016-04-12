#!/usr/bin/env python
# coding=utf-8

import unicodedata
from sys import maxunicode

punctuations = []

for i in range(maxunicode + 1):
    if unicodedata.category(unichr(i))[0] == 'P':
        punctuations.append(unichr(i))


def is_punctuation(token):
    for c in token:
        if c not in punctuations:
            return False

    return True
