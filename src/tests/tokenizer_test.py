#!/usr/bin/env python
# coding=utf-8

import unittest

from tokenizer import tokenizer


class TestGujTokenizer(unittest.TestCase):
    t = tokenizer('guj', split_sentence=True)

    def test_tokens(self):
        self.assertEqual(
            self.t.tokenize(u"તેમનું નામ ડો. બી. પરમાર (Dr. B. Parmar) છે."),
            [[u"તેમનું", u"નામ", u"ડો.", u"બી.", u"પરમાર", u"(", u"Dr.", u"B.",
                u"Parmar", u")", u"છે", u"."]]
        )

    def test_sentences(self):
        self.assertEqual(
            self.t.tokenize(u"તેમનું નામ ડૉ. બી. પરમાર (Dr. B. Parmar) છે. " +
                            u"તેઓ એક જાણીતા ડૉક્ટર છે."),
            [[u"તેમનું", u"નામ", u"ડૉ.", u"બી.", u"પરમાર", u"(", u"Dr.", u"B.",
                u"Parmar", u")", u"છે", u"."],
                [u"તેઓ", u"એક", u"જાણીતા", u"ડૉક્ટર", u"છે", u"."]]
        )

    def test_email(self):
        self.assertEqual(
            self.t.tokenize(u"મારું ઈ-મેલ સરનામું someone@example.com છે."),
            [[u"મારું", u"ઈ-મેલ", u"સરનામું", u"someone@example.com",
                u"છે", u"."]]
        )


class TestTokenizer(unittest.TestCase):
    t = tokenizer(split_sentence=True)

    def test_language_identification(self):
        self.t.tokenize(u"તેમનું નામ ડો. બી. પરમાર (Dr. B. Parmar) છે."),
        self.assertEqual(self.t.lang, 'guj')
        self.assertEqual(self.t.script, 'gujr')
