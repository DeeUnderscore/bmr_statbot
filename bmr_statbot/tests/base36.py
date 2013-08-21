"""
tests/importer.py

Tests of the bmr_statbot.scraper module.
"""

import unittest
from bmr_statbot import recommender

class Base36(unittest.TestCase):
    """
    Tests recommender.to_base36 for proper int/long to base36 encoding
    """
    
    def setUp(self):        
        self.numbers = [(5, '5'),
                        (1500, '15o'),
                        (15000000, '8xi2o'),
                        (15000000L, '8xi2o')]
        
    def test_base36_conversion(self):
        
        for number, output in self.numbers:
            self.assertEqual(output, recommender.to_base36(number))
        
    def test_nonnumber(self):
        
        self.assertRaises(TypeError, recommender.to_base36, None)
        self.assertRaises(TypeError, recommender.to_base36, 'potato')
        
            
