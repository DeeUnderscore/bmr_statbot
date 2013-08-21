"""
tests/importer.py

Tests of the bmr_statbot.scraper module.
"""

import unittest
from bmr_statbot import importer

class URLBreakdownTest(unittest.TestCase):
    """
    Tests importer.chop_multireddit_url
    """
    
    def setUp(self):        
        self.valid_url = 'http://reddit.com///r//example+null+reddit.com+t:1950s/'
        self.non_mr_url = 'http://www.reddit.com/r/pics/comments/92dd8/test_post_please_ignore/'
        
    def test_valid_url(self):
        chopped = importer.chop_multireddit_url(self.valid_url)
        
        for sub in ['example', 'null', 'reddit.com', 't:1950s']:
            self.assertIn(sub, chopped)
        
        self.assertNotIn('+', chopped)
        
    def test_invalid_url(self):
        with self.assertRaises(importer.InvalidMultiredditUrl):
            _ = importer.chop_multireddit_url(self.non_mr_url)
        
        
            
