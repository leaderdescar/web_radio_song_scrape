'''
Created on Jan 5, 2019

@author: papa
'''
import pathlib
import unittest
from radio_webscraper.parser import Parser
import logging


class TestWeb(unittest.TestCase):


    def test_browser(self):
        page = Parser()
        self.assertIsNotNone(page, 'error getting page')
    
    def test_page_parse(self):
        cur_dir = str(pathlib.Path.cwd())
        
        if '/tests' in cur_dir:
            cur_dir=cur_dir.replace('''/tests''', '')
            
        page = open(cur_dir+'/data/sample_songlist.html')
        song_instance = Parser.parse_webpage(self, page, 1111, 1111, 'text')
        
        self.assertEqual(song_instance.song, 'New York City Cops', 'song does not match')  

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_webconnect']
    unittest.main()