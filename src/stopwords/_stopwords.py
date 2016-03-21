#!/usr/bin/env python
# coding=utf-8

import os.path
import cPickle


class stopwords:
    def __init__(self, lang):
        self.lang = lang

    def _get_list_file(self, mode='r'):
        filename = '%s_stopwords.pickle' % self.lang
        filepath = os.path.join(os.path.dirname(__file__), 'data', filename)
        return open(filepath, mode)

    def train(self, words, top_k=50):
        word_list = {}

        for word in words:
            if word not in word_list:
                word_list[word] = 0

            word_list[word] += 1

        words_sorted = sorted(word_list.items(),
                              key=lambda x: x[1],
                              reverse=True)

        stopwords = map(lambda x: x[0], words_sorted[:top_k])

        list_file = self._get_list_file('wb')
        cPickle.dump(stopwords, list_file)

    def inspect(self):
        list_file = self._get_list_file('rb')
        stopwords = cPickle.load(list_file)
        for word in stopwords:
            print word.encode('utf-8')

    def remove(self, sentences):
        list_file = self._get_list_file('rb')
        stopwords = cPickle.load(list_file)

        clean_sentences = []
        for sent in sentences:
            clean_sentences.append(
                [token for token in sent if token not in stopwords]
            )

        return clean_sentences
