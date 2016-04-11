#!/usr/bin/env python
# coding=utf-8


def print_report(data, correct='correct',
                 total_tagged='total_tagged',
                 total_in_gold='total_in_gold'):
    """
    data is a dict() with tags as key and
    a dict containing `correct`, `total_tagged` and `total_in_gold` as value

    `correct`, key storing the correct classifications
    `total_tagged`, key storing the number of samples classified to this class
    `total_in_gold `, key storing number of sample of this class in gold data
    """

    summary = {
        'correct': 0,
        'total_tagged': 0,
        'total_in_gold': 0
    }

    for classname in data:
        summary['correct'] += data[classname][correct]
        summary['total_tagged'] += data[classname][total_tagged]
        summary['total_in_gold'] += data[classname][total_in_gold]

        precision = data[classname][correct] / \
            float(data[classname][total_tagged]) \
            if data[classname][total_tagged] else 0

        recall = data[classname][correct] / \
            float(data[classname][total_in_gold]) \
            if data[classname][total_in_gold] else 0

        fscore = 2 * precision * recall / float(precision + recall) \
            if precision + recall else 0

        print '%15s\t%.2f\t%.2f\t%.2f\t%d' % (classname, precision * 100,
                                              recall * 100, fscore * 100,
                                              data[classname][total_in_gold])

    precision = summary['correct'] / float(summary['total_tagged']) \
        if summary['total_tagged'] else 0
    recall = summary['correct'] / float(summary['total_in_gold']) \
        if summary['total_in_gold'] else 0
    fscore = 2 * precision * recall / float(precision + recall) \
        if precision + recall else 0

    print 'F-score: %.2f%% (precision: %.2f%%, recall: %.2f%%)'\
        % (
            fscore * 100,
            precision * 100,
            recall * 100
        )
