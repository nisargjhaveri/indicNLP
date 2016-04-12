#!/usr/bin/env python
# coding=utf-8

import unittest
import os.path


def run_all():
    testdir_path = os.path.dirname(__file__)
    suite = unittest.TestLoader().discover(
        testdir_path,
        pattern='*_test.py',
        top_level_dir=os.path.normpath(os.path.join(testdir_path, '..', '..'))
    )
    unittest.TextTestRunner(verbosity=2).run(suite)
