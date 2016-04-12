#!/usr/bin/env python
# coding=utf-8

import os.path
import json


class NewsCategory_Corpus:
    def __init__(self, lang):
        self.lang = lang
        self.load_file()

    def load_file(self):
        datapath = os.path.join(os.path.dirname(__file__), 'data', 'newscat')
        filename = '_'.join([self.lang, 'news.data'])
        self.datafile = open(os.path.join(datapath, filename))

    def articles(self, start=None, end=None):
        i = 0
        for rawline in self.datafile:
            line = rawline.decode('utf-8')
            article = json.loads(line)

            if 'url' not in article \
                    or 'text' not in article \
                    or 'title' not in article \
                    or 'mCategory' not in article:
                continue

            i += 1

            if start is not None and i < start:
                continue
            elif end is not None and i >= end:
                continue

            yield article


def load(lang):
    return NewsCategory_Corpus(lang)
