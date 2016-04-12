#!/usr/bin/env python
# coding=utf-8

from ..stopwords import stopwords
from ..datasets import ilci_corpus


def train(lang):
    corpus_h = ilci_corpus.load(lang, 'health')
    corpus_t = ilci_corpus.load(lang, 'tourism')

    words = []
    for tokens in corpus_h.tokens():
        words.append(tokens[0])
    for tokens in corpus_t.tokens():
        words.append(tokens[0])

    s = stopwords(lang)

    s.train(words)
