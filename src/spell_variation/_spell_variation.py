#!/usr/bin/env python
# coding=utf-8

import os.path
import re


class Rule:
    def __init__(self, rule):
        self.find = rule[0]
        self.replace = rule[1]
        self.penalty = int(rule[2])

    def apply(self, word):
        word, n = re.subn(self.find, self.replace, word, flags=re.UNICODE)
        # penalty = n * self.penalty

        return word


class variation_identifier:
    def __init__(self, lang):
        self.lang = lang

        self._load_rules()

    def _load_rules(self):
        self.rules = []
        rulesfile = self._get_rules_file()

        for rawline in rulesfile:
            line = rawline.decode('utf-8')
            # Allow comments with '#'
            rule = line.split('#')[0].strip()
            if not rule:
                continue

            rule = rule.split('\t')
            if len(rule) != 3:
                continue

            self.rules.append(Rule(rule))

    def _get_rules_file(self, mode='r'):
        filename = '%s_variation.rules' % self.lang
        filepath = os.path.join(os.path.dirname(__file__), 'data', filename)
        return open(filepath, mode)

    def are_same(self, word1, word2):
        for rule in self.rules:
            if word1 == word2:
                break
            word1 = rule.apply(word1)
            word2 = rule.apply(word2)

        if word1 == word2:
            return True
        else:
            return False
