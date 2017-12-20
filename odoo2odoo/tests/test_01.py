# -*- coding: utf-8 -*-

import unittest


class test_backend(unittest.TestCase):
    """ Test Backend """

    def setUp(self):
        super(test_backend, self).setUp()

    def test_new_backend(self):
        self.assertEqual(1,1)