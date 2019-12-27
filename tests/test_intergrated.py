'''
Created on Dec 23, 2019

@author: papa
'''
import pathlib
import unittest
import logging
import pandas
from datetime import datetime
from bs4 import BeautifulSoup
from radio_webscraper.utils import Utils
from radio_webscraper.db_interface.dao import DBConnection
from radio_webscraper.browser import browser_engine as be
from radio_webscraper.parsers.triton_parser import TritonParser
from radio_webscraper.processor.song_insert_engine import SongInsertEngine

class TestIntergration(unittest.TestCase):


    def setUp(self):
        
        Utils.initialize_logging()
        
        db_config = Utils.get_config()
        self.cnx = DBConnection(db_config['user'], 
                                 db_config['password'],
                                 db_config['host'], 
                                 db_config['database'],
                                 db_config['schema'])
        self.cnx.create_cnx_pool()
        self.cnx.get_connection()

        self.browser = be.BrowserEngine().get_browser()

        #create test dataframe
        cur_dir = str(pathlib.Path.cwd())
        
        if '/tests' in cur_dir:
            cur_dir=cur_dir.replace('''/tests''', '')

        self.tri_page = open(cur_dir+'/data/617_sample.html')

        self.tri_parse = TritonParser()

        triton_song_block=self.tri_parse.get_triton_songs_block(self.tri_page)
        song_dict_list=self.tri_parse.get_triton_songs_list(triton_song_block)
        self.test_song_df=self.tri_parse.convert_triton_list_to_df(song_dict_list)

        #clean out previous test in case of failure
        self.cnx.del_test_song_instances()
        #insert dummy test row for max timestamp testing get midway
        self.cnx.insert_song_instance(1,1,'2019-12-15 22:59:11')

    def tearDown(self):

        #add clean up of song instance
        self.cnx.del_test_song_instances()
        self.cnx.close_connection()

    def test_get_617_page(self):
        url=self.cnx.get_station_url('921')
        self.browser.get(url)
        self.assertTrue('indie617' in self.browser.title, 'Issue geting 617 song history page')

    def test_get_triton_song_section(self):
        url=self.cnx.get_station_url('921')
        tri_pars = TritonParser()
        song_df=tri_pars.get_triton_df(url)

        self.assertTrue(len(song_df)>0, "Issue parseing page")

    def test_df_timestamp_conversion(self):
        df=Utils.convert_df_milisec_to_timestamp(self.test_song_df)
        song_ts=df.iloc[0,0]
        test_ts=datetime.strptime('2019-12-15 22:21:05','%Y-%m-%d %H:%M:%S')
        self.assertTrue(song_ts==test_ts,'Issue with converting milliscoend to timestamp')

    def test_df_timestamp_filter(self):
        sie=SongInsertEngine()
        df=Utils.convert_df_milisec_to_timestamp(self.test_song_df)
        df=sie.filter_df_by_web_id_time(df,1)
        self.assertTrue(len(df.index)==9, 'Issue with filtering dataframe by timestamp')

    def test_bulk_song_instance_inserts(self):
        sie=SongInsertEngine()
        df=Utils.convert_df_milisec_to_timestamp(self.test_song_df)
        df=sie.filter_df_by_web_id_time(df,1)
        sie.process_song_instances(df,1)
        insert_cnt=self.cnx.get_test_song_instance_cnt()
        #number of filter rows plus inserted row for filter
        self.assertTrue(insert_cnt==10,'Issue inserting song instances')




