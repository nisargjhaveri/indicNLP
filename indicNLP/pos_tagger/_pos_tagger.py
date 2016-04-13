#!/usr/bin/env python
# coding=utf-8

import os.path
import cPickle

import pycrfsuite

from ..common import features as feature_lib


class pos_tagger:
    def __init__(self, lang, model_name, feature_functions=None):
        self.lang = lang
        self.model_name = model_name

        self._feature_lib_extend = feature_functions
        self._feature_list = None
        self._feature_func = None

        self._tagger = pycrfsuite.Tagger()
        self._model_loaded = False

        # Try to load model, if already exists
        self._load_model()

    def _get_feature_func(self, feature_list):
        def _get_feature_func_by_name(feature_name):
            _feature_lib_ext = self._feature_lib_extend
            if _feature_lib_ext is not None:
                feature_func = getattr(_feature_lib_ext, feature_name, None)
                if hasattr(feature_func, '__call__'):
                    return feature_func

            feature_func = getattr(feature_lib, feature_name, None)
            if hasattr(feature_func, '__call__'):
                return feature_func

            raise NotImplementedError(
                'Could not find feature "' + feature_name + '"'
                )

        def extract_features(tokens, i):
            features = []
            for feature in feature_list:
                feature_parse = feature.split(':')
                feature_name = feature_parse[0]
                feature_args = [tokens, i] + feature_parse[1:]

                feature_func = _get_feature_func_by_name(feature_name)

                features.extend(feature_func(*feature_args))

            return features

        return extract_features

    def _get_model_file(self):
        current_path = os.path.dirname(__file__)
        modelfile = '%s/data/%s_%s.model' % (current_path,
                                             self.lang,
                                             self.model_name)
        return modelfile

    def _get_feature_file(self):
        current_path = os.path.dirname(__file__)
        featurefile = '%s/data/%s_%s.features' % (current_path,
                                                  self.lang,
                                                  self.model_name)

        return featurefile

    def _load_feature_list(self):
        featurefile = open(self._get_feature_file(), 'rb')
        feature_list = cPickle.load(featurefile)
        featurefile.close()

        self._set_feature_list(feature_list)

    def _store_feature_list(self):
        featurefile = open(self._get_feature_file(), 'wb')
        cPickle.dump(self._feature_list, featurefile, 2)
        featurefile.close()

    def _set_feature_list(self, feature_list):
        self._feature_list = feature_list
        self._feature_func = self._get_feature_func(feature_list)

    def _load_model(self):
        modelfile = self._get_model_file()
        if not os.path.isfile(modelfile):
            return

        # if already loaded, close
        if self._model_loaded:
            self._tagger.close()

        # Open model
        self._tagger.open(modelfile)
        # Load features for the model
        self._load_feature_list()

        self._model_loaded = True

    def train(self, train_data, feature_list):
        self._set_feature_list(feature_list)

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
        # Store features for the model
        self._store_feature_list()

        # Once training is done, load the model
        self._load_model()

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
