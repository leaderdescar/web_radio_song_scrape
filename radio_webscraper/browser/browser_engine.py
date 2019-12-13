from selenium import webdriver
from radio_webscraper.utils import Utils
import logging

class BrowserEngine(object):
    def __init__(self):
        '''
        Constructor
        '''
        
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        self.browser = webdriver.Chrome(chrome_options=options)
        
    def get_browser(self):
        return self.browser

