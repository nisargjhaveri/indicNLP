#!/usr/bin/env python
# coding=utf-8

import os.path

import pycrfsuite


class pos_tagger:
    def __init__(self, lang, model_name, features):
        self.lang = lang
        self.model_name = model_name

        if hasattr(features, '__call__'):
            self._feature_func = features
        else:
            self._feature_func = self._get_feature_func(features)

        self._tagger = pycrfsuite.Tagger()
        self._model_loaded = False

        # Try to load model, if already exists
        self._load_model_file()

    def _get_feature_func(self, features):
        raise NotImplementedError

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

        # if already loaded, close
        if self._model_loaded:
            self._tagger.close()

        # Open model
        self._tagger.open(modelfile)
        self._model_loaded = True

    def train(self, train_data):
        trainer = pycrfsuite.Trainer(verbose=True)
        print "Training parameters"
        print trainer.get_params()

        # trainer.set_params(self._training_options)

        for sent in train_data:
            if not sent:
                continue
            tokens, labels = zip(*sent)
            features = [self._feature_func(tokens, i)
                        for i in range(len(tokens))]
            trainer.append(features, labels)

        # Train and store model
        trainer.train(self._get_model_file())

        # Once training is done, load the model
        self._load_model_file()

    def tag(self, sentences):
        # If no model is loaded, error
        if not self._model_loaded:
            raise Exception('Model is not loaded, you need to train first')

        result = []
        for tokens in sentences:
            features = [self._feature_func(tokens, i)
                        for i in range(len(tokens))]

            labels = self._tagger.tag(features)

            tagged_sent = list(zip(tokens, labels))
            result.append(tagged_sent)

        return result
