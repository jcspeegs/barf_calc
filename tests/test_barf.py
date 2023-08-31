#!/usr/bin/env python3

""" BARFCalc tests"""

import unittest
from barf_calc import Food


class TestPresets(unittest.TestCase):
    """Test validitiy of presets"""

    def test_valid_instance(self):
        """Test that each preset item creates a valid Food instance"""
        for cfg in Food.presets:
            item = Food(1, **cfg)
            self.assertIsInstance(item, Food)

        del item

    def test_sum_of_parts(self):
        """Test sum of item composition is 1"""
        for cfg in Food.presets:
            total_pct = 0.0
            for ingredient in cfg.values():
                try:
                    total_pct += ingredient
                except TypeError:
                    pass
            self.assertEqual(1.0, total_pct)

        del total_pct

    def test_ge0(self):
        """Test no individual component <0"""
        pass

    def test_get_preset(self):
        """Test get_preset function returns an integer which corresponds to
        an item in the presets file
        """
        pass


class TestAddMethod(unittest.TestCase):
    """Test the add method"""

    def setUp(self):
        """Add item for testing"""
        Food.add(1, {"description": "Test Item #1"})
        Food.add(11.123, {"description": "Test Item #2"})

    def test_registrylength_onadd(self):
        """Test Food._registry grows in length after add method is used"""
        self.assertEqual(2, len(Food._registry))

    def test_registryobj_onadd(self):
        """Test _registry receives valid Food instance on add method"""
        for i in range(2):
            self.assertIsInstance(Food._registry[i], Food)

    def test_weight_total(self):
        """Test total item weight is correctly aggregated on add method"""
        self.assertEqual(12.123, Food._total_wt["weight"])

    def tearDown(self):
        """Undo the add method"""
        Food._registry = []
        Food._total_wt = {
            "weight": 0.0,
            "bone": 0.0,
            "meat": 0.0,
            "vege": 0.0,
            "fruit": 0.0,
            "organ": 0.0,
        }


class TestGetWeight(unittest.TestCase):
    """Test get_item_weight function"""

    def test_get_item_weight(self):
        """get_item_weight function returns input as float"""
        qa = [(3.1, 3.1), (3.0, 3)]
        for y, x in qa:
            weight = Food.get_item_weight(x)
            self.assertEqual(y, weight)

        del qa


if __name__ == "__main__":
    unittest.main()
