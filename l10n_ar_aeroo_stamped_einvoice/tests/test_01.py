# -*- coding: utf-8 -*-

import unittest


class TestBackend(unittest.TestCase):
    """ Test Backend """

    def setUp(self):
        super(TestBackend, self).setUp()

    def test_new_backend(self):
        self.assertEqual(1, 1)
