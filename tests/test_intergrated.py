'''
Created on Dec 23, 2019

@author: papa
'''
import pathlib
import unittest
import logging
import pandas
from bs4 import BeautifulSoup
from radio_webscraper.utils import Utils
from radio_webscraper.db_interface.dao import DBConnection
from radio_webscraper.browser import browser_engine as be
from radio_webscraper.parsers.triton_parser import TritonParser

class TestIntergration(unittest.TestCase):


    def setUp(self):
        
        Utils.initialize_logging(self)
        
        db_config = Utils.get_config(self)
        self.cnx = DBConnection(db_config['user'], 
                                 db_config['password'],
                                 db_config['host'], 
                                 db_config['database'],
                                 db_config['schema'])
        self.cnx.create_cnx_pool()
        self.cnx.get_connection()

        self.browser = be.BrowserEngine().get_browser()

    def test_get_617_page(self):
        url=self.cnx.get_station_url('921')
        self.browser.get(url)
        self.assertTrue('indie617' in self.browser.title, 'Issue geting 617 song history page')

    def test_get_triton_song_section(self):
        url=self.cnx.get_station_url('921')
        tri_pars = TritonParser()
        #source_page=tri_pars.get_triton_page(url)
        song_df=tri_pars.get_triton_df(url)

        self.assertTrue(len(song_df)>0, "Issue parseing page")

    