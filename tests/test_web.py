'''
Created on Jan 5, 2019

@author: papa
'''
import pathlib
import unittest

from radio_webscraper.browser import browser_engine as be
import logging


class TestWeb(unittest.TestCase):

    def test_browser_engine(self):
        browser = be.BrowserEngine()
        self.assertIsNotNone(browser,'error starting browser')
    
    def test_get_page(self):
        browser = be.BrowserEngine().get_browser()
        browser.get('https://en.wikipedia.org/wiki/Web_navigation')
        print(str(browser.title))

        self.assertTrue('Web' in browser.title,'Issue getting web page')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_webconnect']
    unittest.main()