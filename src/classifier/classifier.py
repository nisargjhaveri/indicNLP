#!/usr/bin/env python
# coding=utf-8

import os.path
import cPickle

from .naive_bayes import NaiveBayes


class classifier:
    def __init__(self, lang, model_name):
        self.lang = lang
        self.model_name = model_name

        self._classifier = NaiveBayes()
        self._model_loaded = False

        # Try to load model, if already exists
        self._load_model_file()

    def _get_model_file(self):
        current_path = os.path.dirname(__file__)
        modelfile = '%s/data/%s_%s.model' % (current_path,
                                             self.lang,
                                             self.model_name)
        return modelfile

    def _load_model_file(self):
        modelfile = self._get_model_file()
        if not os.path.isfile(modelfile):
            return

        # Open model
        with open(modelfile, 'rb') as model:
            modeldata = cPickle.load(model)
            self._classifier.load_model(modeldata)
            self._model_loaded = True

    def _save_model_file(self, modeldata):
        modelfile = self._get_model_file()

        # Save model
        with open(modelfile, 'wb') as model:
            cPickle.dump(modeldata, model, 2)

    def train(self, train_data):
        for featureset, class_name in train_data:
            self._classifier.train(featureset, class_name)

        self._save_model_file(self._classifier.get_model())

    def classify(self, featureset):
        # If no model is loaded, error
        if not self._model_loaded:
            raise Exception('Model is not loaded, you need to train first')

        return self._classifier.classify(featureset)
