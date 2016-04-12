#!/usr/bin/env python
# coding=utf-8

import os.path
import cPickle

from ._punctuations import is_punctuation


class stopwords:
    def __init__(self, lang):
        self.lang = lang

        self._stopwords = None
        self._load_list_file()

    def _get_list_file(self, mode='r'):
        filename = '%s_stopwords.pickle' % self.lang
        filepath = os.path.join(os.path.dirname(__file__), 'data', filename)

        if not os.path.isfile(filepath):
            return None

        return open(filepath, mode)

    def _load_list_file(self):
        list_file = self._get_list_file('rb')
        if not list_file:
            return

        self._stopwords = cPickle.load(list_file)
        list_file.close()

    def train(self, words, top_k=50):
        word_list = {}

        for word in words:
            if is_punctuation(word):
                continue

            if word not in word_list:
                word_list[word] = 0

            word_list[word] += 1

        words_sorted = sorted(word_list.items(),
                              key=lambda x: x[1],
                              reverse=True)

        stopwords = map(lambda x: x[0], words_sorted[:top_k])

        list_file = self._get_list_file('wb')
        cPickle.dump(stopwords, list_file, 2)
        list_file.close()

        self._load_list_file()

    def inspect(self):
        if not self._stopwords:
            raise Exception(
                'Stopword list does not exist, you need to train first'
            )

        for word in self._stopwords:
            print word.encode('utf-8')

    def remove(self, sentences):
        if not self._stopwords:
            raise Exception(
                'Stopword list does not exist, you need to train first'
            )

        clean_sentences = []
        for sent in sentences:
            clean_sentences.append(
                [token
                    for token in sent if
                    token not in self._stopwords and
                    not is_punctuation(token)]
            )

        return clean_sentences
