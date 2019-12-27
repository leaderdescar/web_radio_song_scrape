'''
Created on Dec 14, 2019

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
from radio_webscraper.parsers.old_parser import OldParser



class TestParsing(unittest.TestCase):


    def setUp(self):
        
        Utils.initialize_logging()

        cur_dir = str(pathlib.Path.cwd())
        
        if '/tests' in cur_dir:
            cur_dir=cur_dir.replace('''/tests''', '')
            
        self.tri_page = open(cur_dir+'/data/617_sample.html')
        
        self.browser = be.BrowserEngine().get_browser()
        self.tri_parse = TritonParser()
    
    def test_triton_parse_songs_block(self):
        triton_song_block=self.tri_parse.get_triton_songs_block(self.tri_page)
        self.assertTrue('1576448465000' in triton_song_block, 'Issue get song block')

    def test_triton_parse_song_list(self):
        triton_song_block=self.tri_parse.get_triton_songs_block(self.tri_page)
        song_dict_list=self.tri_parse.get_triton_songs_list(triton_song_block)
        self.assertTrue(song_dict_list[0]['title']=='Fluttering In The Floodlights', 'Issue converting to list')

    def test_triton_remove_song_keys(self):
        temp_dict={'title':'Song Title','trackId':'12365458','album':'Album Title'}
        temp_dict=self.tri_parse.remove_triton_song_keys(temp_dict)
        self.assertFalse('trackId' in temp_dict, 'Issue removing key from dictionary in list')
    
    def test_triton_parse_df(self):
        triton_song_block=self.tri_parse.get_triton_songs_block(self.tri_page)
        song_dict_list=self.tri_parse.get_triton_songs_list(triton_song_block)
        song_df=self.tri_parse.convert_triton_list_to_df(song_dict_list)
        column_list=list(song_df.columns.values)
        self.assertTrue(column_list[1]=='song_name', 'Issue changing name of columns')
        self.assertTrue(song_df.iloc[0,1]=='Fluttering In The Floodlights', 'Issue getting dataframe')




    #old parser tests

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
