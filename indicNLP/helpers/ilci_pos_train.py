#!/usr/bin/env python
# coding=utf-8

from ..pos_tagger import pos_tagger
from ..datasets import ilci_corpus
from ..common.fscore import print_report


def get_model_name():
    return "words_i_pre_3_suf_5_len_relpos_context_2"


def get_feature_list():
    return ['token', 'pos', 'relpos', 'lenght', 'prefix:1', 'prefix:2',
            'prefix:3', 'suffix:1', 'suffix:2', 'suffix:3', 'suffix:4',
            'suffix:5', 'context:1', 'context:2', 'context:-1', 'context:-2']


def train(lang, domain, model_name, feature_list):
    corpus = ilci_corpus.load(lang, domain)

    sentences = []
    for sent in corpus.sentences():
        sentences.append(sent)

    train_set = sentences[:17500]
    # dev_set = sentences[17500:21250]
    # test_set = sentences[21250:]

    pos = pos_tagger(lang, '%s_ilci_%s' % (domain, model_name))
    pos.train(train_set, feature_list)


def evaluate(lang, domain, model_name):
        corpus = ilci_corpus.load(lang, domain)

        sentences = []
        for sent in corpus.sentences():
            sentences.append(sent)

        # train_set = sentences[:17500]
        dev_set = sentences[17500:21250]
        # test_set = sentences[21250:]

        pos = pos_tagger(lang, '%s_ilci_%s' % (domain, model_name))
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


def run_all(lang):
    model_name = get_model_name()
    feature_list = get_feature_list()

    train(lang, 'health', model_name, feature_list)
    train(lang, 'tourism', model_name, feature_list)

    evaluate(lang, 'health', model_name)
    evaluate(lang, 'tourism', model_name)
