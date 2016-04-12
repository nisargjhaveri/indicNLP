#!/usr/bin/env python
# coding=utf-8

from ..datasets import newscat_corpus
from ..tokenizer import tokenizer
from ..stopwords import stopwords
from ..classifier import classifier
from ..common.fscore import print_report

samples_len = {
    'hin': 114678,
    'guj': 70990
}
categories = {
    'guj': set([u'criminals', u'business', u'entertainment', u'travel',
                u'sports', u'automobiles', u'foods', u'politics',
                u'technology']),
    'hin': set([u'fashion', u'business', u'entertainment', u'travel',
                u'sports', u'automobiles', u'foods', u'criminals', u'health',
                u'politics', u'technology'])
}


def train(lang):
    corpus = newscat_corpus.load(lang)

    train_samples = int(samples_len[lang] * 0.80)

    t = tokenizer(lang, False)
    s = stopwords(lang)
    c = classifier(lang, 'newscat')

    def train_data():
        for i, article in enumerate(corpus.articles(end=train_samples)):
            featureset = map(lambda x: 't_' + x,
                             s.remove(t.tokenize(article['title']))[0]) + \
                         s.remove(t.tokenize(article['text']))[0]

            class_name = article['mCategory']

            print i, '\r',
            yield (featureset, class_name)

        print

    c.train(train_data())


def evaluate(lang):
    corpus = newscat_corpus.load(lang)

    train_samples = int(samples_len[lang] * 0.80)

    t = tokenizer(lang, False)
    s = stopwords(lang)
    c = classifier(lang, 'newscat')

    result_matrix = {}

    for i, article in enumerate(corpus.articles(start=train_samples)):
        featureset = map(lambda x: 't_' + x,
                         s.remove(t.tokenize(article['title']))[0]) + \
                     s.remove(t.tokenize(article['text']))[0]

        correct_class = article['mCategory']

        print i, '\r',
        class_probabilities = c.classify(featureset)

        if class_probabilities[0][1]:
            guessed_class = class_probabilities[0][0]
        else:
            guessed_class = None

        if correct_class not in result_matrix:
            result_matrix[correct_class] = {
                'correct': 0,
                'total_tagged': 0,
                'total_in_gold': 0
            }

        if guessed_class and guessed_class not in result_matrix:
            result_matrix[guessed_class] = {
                'correct': 0,
                'total_tagged': 0,
                'total_in_gold': 0
            }

        if guessed_class:
            result_matrix[guessed_class]['total_tagged'] += 1

        result_matrix[correct_class]['total_in_gold'] += 1

        if guessed_class and guessed_class == correct_class:
            result_matrix[guessed_class]['correct'] += 1

    print ' ' * 20
    print_report(result_matrix)
