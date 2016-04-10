#!/usr/bin/env python
# coding=utf-8

from ..pos_tagger import pos_tagger
from ..datasets import ilci_corpus
from ..common.fscore import print_report


def get_model_name():
    return "words_i_pre_suf_3_context_2"


def extract_features(tokens, i):
    return set([tokens[i],
                'i_' + str(i),
                'pre_' + tokens[i][:1],
                'pre_' + tokens[i][:2],
                'pre_' + tokens[i][:3],
                'suf_' + tokens[i][-1:],
                'suf_' + tokens[i][-2:],
                'suf_' + tokens[i][-3:],
                '-1_' + tokens[i - 1] if i >= 1 else 'start'
                '-2_' + tokens[i - 2] if i >= 2 else 'start'
                '+1_' + tokens[i + 1] if i + 1 < len(tokens) else 'end'
                '+2_' + tokens[i - 2] if i + 2 < len(tokens) else 'end'
                ])


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


def run_all(lang):
    model_name = get_model_name()

    train(lang, 'health', model_name)
    train(lang, 'tourism', model_name)

    evaluate(lang, 'health', model_name)
    evaluate(lang, 'tourism', model_name)
