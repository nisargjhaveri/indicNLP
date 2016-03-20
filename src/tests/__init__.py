#!/usr/bin/env python
# coding=utf-8

import unittest
import os.path


def run_all():
    suite = unittest.TestLoader().discover(
        os.path.dirname(__file__),
        pattern='*_test.py'
    )
    unittest.TextTestRunner(verbosity=2).run(suite)
