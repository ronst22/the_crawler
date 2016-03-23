#!/usr/bin/python

import os
from Offensive import Offensive
import unittest

offensive = Offensive()

class TestRealClasifier(unittest.TestCase):
    def test_clasi_pos(self):
        self.assertTrue(offensive.is_offensive("the good life"))

    def test_clasi_neg(self):
        self.assertFalse(offensive.is_offensive("ass fuck"))

    def test_clasi_neg_pos(self):
        self.assertFalse(offensive.is_offensive("you are a fucking ass and you are really good piss of shit"))

    def test_clasi_sexual_1(self):
        self.assertFalse(offensive.is_offensive("I wanna fuck you"))

    def test_clasi_sexual_2(self):
        self.assertFalse(offensive.is_offensive("You have nice tits and ass"))

if __name__ == '__main__':
    unittest.main()