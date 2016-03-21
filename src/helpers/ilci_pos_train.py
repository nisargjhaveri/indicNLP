#!/usr/bin/env python
# coding=utf-8

from ..pos_tagger import pos_tagger
from ..datasets import ilci_corpus
from ..common.fscore import print_report


def extract_features(tokens, i):
    return [tokens[i]]


def train(lang, domain, model_name):
    corpus = ilci_corpus.load(lang, domain)

    sentences = []
    for sent in corpus.sentences():
        sentences.append(sent)

    train_set = sentences[:17500]
    # dev_set = sentences[17500:21250]
    # test_set = sentences[21250:]

    pos = pos_tagger(lang, '%s_ilci_%s' % (domain, model_name),
                     extract_features)
    pos.train(train_set)

    evaluate(lang, domain, model_name)


def evaluate(lang, domain, model_name):
        corpus = ilci_corpus.load(lang, domain)

        sentences = []
        for sent in corpus.sentences():
            sentences.append(sent)

        # train_set = sentences[:17500]
        dev_set = sentences[17500:21250]
        # test_set = sentences[21250:]

        pos = pos_tagger(lang, '%s_ilci_%s' % (domain, model_name),
                         extract_features)
        tokens = map(lambda x: zip(*x)[0], dev_set)
        pos_tagged = pos.tag(tokens)

        result_matrix = {}

        for i, sent in enumerate(dev_set):
            result_sent = pos_tagged[i]

            for j, token in enumerate(sent):
                if token[1] not in result_matrix:
                    result_matrix[token[1]] = {
                        'correct': 0,
                        'total_tagged': 0,
                        'total_in_gold': 0
                    }

                if result_sent[j][1] not in result_matrix:
                    result_matrix[result_sent[j][1]] = {
                        'correct': 0,
                        'total_tagged': 0,
                        'total_in_gold': 0
                    }

                result_matrix[result_sent[j][1]]['total_tagged'] += 1
                result_matrix[token[1]]['total_in_gold'] += 1

                if result_sent[j][1] == token[1]:
                    result_matrix[token[1]]['correct'] += 1

        print_report(result_matrix)
