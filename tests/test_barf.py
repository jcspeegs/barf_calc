#!/usr/bin/env python3

import unittest
from barf_calc import Food


class TestPresets(unittest.TestCase):
    def test_presets(self):
        for i in Food.presets:
            item = Food(1, **i)
            self.assertIsInstance(item, Food)
        del item


class TestAdd(unittest.TestCase):
    def setUp(self):
        Food.add(1, {'description': 'Test Item'})

    def test_registrylength_onadd(self):
        self.assertEqual(1, len(Food._registry))

    def test_registryobj_onadd(self):
        self.assertIsInstance(Food._registry[0], Food)

    def tearDown(self):
        Food._registry = []
        Food._total_wt = {'weight': 0., 'bone': 0., 'meat': 0., 'vege': 0.,
                          'fruit': 0., 'organ': 0.}


if __name__ == '__main__':
    unittest.main()
