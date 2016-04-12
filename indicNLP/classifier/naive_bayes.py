#!/usr/bin/env python
# coding=utf-8

from math import log


class NaiveBayes:
    def __init__(self):
        # classname: frequancy
        self.classes = {}
        # feature, classname: frequancy
        self.features = {}

        self.default_prob = 0.0000000001

    def get_model(self):
        return {
            'classes': self.classes,
            'features': self.features
        }

    def load_model(self, model):
        self.classes = model['classes']
        self.features = model['features']

    def train(self, features, classname):
        self.classes[classname] = self.classes.get(classname, 0) + 1

        for feature in features:
            if feature not in self.features:
                self.features[feature] = {}

            self.features[feature][classname] = \
                self.features[feature].get(classname, 0) + 1

    def _get_prior(self, classname):
        return self.classes[classname] / float(sum(self.classes.values()))

    def _get_classes(self):
        return self.classes.keys()

    def _get_probability(self, feature, classname):
        if feature not in self.features or \
                classname not in self.features[feature]:
            return self.default_prob

        return self.features[feature][classname] / \
            float(self.classes[classname])

    def classify(self, features):
        class_probabilities = {}

        for classname in self._get_classes():
            class_probabilities[classname] = log(self._get_prior(classname))

            for feature in features:
                class_probabilities[classname] += \
                    log(self._get_probability(feature, classname))

        return sorted(class_probabilities.items(),
                      key=lambda x: x[1],
                      reverse=True)
