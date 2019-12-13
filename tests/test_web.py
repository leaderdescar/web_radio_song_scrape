'''
Created on Jan 5, 2019

@author: papa
'''
import pathlib
import unittest
from radio_webscraper.parsers.old_parser import OldParser
from radio_webscraper.browser import browser_engine as be
import logging


class TestWeb(unittest.TestCase):

    def test_browser_engine(self):
        browser = be.BrowserEngine()
        self.assertIsNotNone(browser,'error starting browser')
    
    def test_get_page(self):
        browser = be.BrowserEngine().get_browser()
        browser.get('https://en.wikipedia.org/wiki/Web_navigation')
        driver_logs = browser.get_log('browser')
        #browser.implicitly_wait(100)
        for log in driver_logs:
            print(log)
        assert 'Web' in browser.title

        self.assertTrue(True,'Issue getting web page')



    def test_old_browser_method(self):
        page = OldParser()
        self.assertIsNotNone(page, 'error getting page')

    def test_page_parse(self):
        cur_dir = str(pathlib.Path.cwd())
        
        if '/tests' in cur_dir:
            cur_dir=cur_dir.replace('''/tests''', '')
            
        page = open(cur_dir+'/data/sample_songlist.html')
        song_instance = OldParser.parse_webpage(self, page, 1111, 1111, 'text')
        print(song_instance.song)
        
        self.assertEqual(song_instance.song, 'New York City Cops', 'song does not match')  



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_webconnect']
    unittest.main()