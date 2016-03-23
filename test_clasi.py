#!/usr/bin/python

import os
from Offensive import Offensive
import pickle
import unittest

offensive = Offensive(clasi=pickle.load(open(os.path.join("test", "movies.pickle"))))

class TestClasifier(unittest.TestCase):
    def test_clasi_pos(self):
        self.assertFalse(offensive.is_offensive(open("test/pos/1.txt", 'rt').read()))

    def test_clasi_neg(self):
        self.assertTrue(offensive.is_offensive(open("test/neg/1.txt", 'rt').read()))

    def test_clasi_not_really_pos(self):
        self.assertTrue(offensive.is_offensive(open("test/pos/not_real.txt", 'rt').read()))

if __name__ == '__main__':
    unittest.main()