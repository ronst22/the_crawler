#!/usr/bin/python
 # -*- coding: utf-8 -*-

import os
from Offensive import Offensive
import unittest

offensive = Offensive()

class TestRealClasifier(unittest.TestCase):
    def test_clasi_pos(self):
        self.assertFalse(offensive.is_offensive("the good life"))

    def test_clasi_neg(self):
        self.assertTrue(offensive.is_offensive("ass fuck"))

    def test_clasi_neg_pos(self):
        self.assertTrue(offensive.is_offensive("you are a fucking ass and you are really good piss of shit"))

    def test_clasi_sexual_1(self):
        self.assertTrue(offensive.is_offensive("I wanna fuck you"))

    def test_clasi_sexual_2(self):
        self.assertTrue(offensive.is_offensive("You have nice tits and ass"))

    def test_clasi_neg_alot(self):
        self.assertTrue(offensive.is_offensive("""In fact, bigrams can make a huge difference,
         but you cant restrict them to just 200 significant collocations.
         Instead you must include all of them and let the scoring function
         decide whats significant and what isn’t.
         ass fuck Of course the Bourne bias is still present with the (matt, damon)
         bigram, but you cant argue with the numbers. Every metric is at greater,
         clearly showing that high information feature selection with bigrams is hugely beneficial
         for text classification, at least when using the the NaiveBayes algorithm."""))

    def test_clasi_neg_html(self):
        self.assertTrue(offensive.is_offensive(""" Comments Edit  ·  Delete Eylon Shabtay     ‎ Yoav Danieli Ass fuck jew fucker 5 mins  ·  Friends of Friends More Like Comment Share Write a comment... Attach a Photo  ·  Mention Friends
"""))

if __name__ == '__main__':
    unittest.main()