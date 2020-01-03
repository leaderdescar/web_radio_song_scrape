'''
Created on Dec 23, 2019

@author: papa
'''
import pathlib
import unittest
import logging
import logging.config
from datetime import datetime
from radio_webscraper.utils import Utils
from radio_webscraper.db_interface.dao import DBConnection
from radio_webscraper.browser import browser_engine as be
from radio_webscraper.parsers.triton_parser import TritonParser
from radio_webscraper.processor.song_insert_engine import SongInsertEngine
from radio_webscraper.processor.scrape_songs_engine import ScrapeSongs

logging.config.fileConfig(fname='config/test_logging.conf', disable_existing_loggers=False)
        
logger=logging.getLogger(__name__)

class TestIntergration(unittest.TestCase):


    def setUp(self):
        


        logger.info('*****Getting DB Conncetion*******')
        db_config = Utils.get_config()
        self.cnx = DBConnection(db_config['user'], 
                                 db_config['password'],
                                 db_config['host'], 
                                 db_config['database'],
                                 db_config['schema'])
        self.cnx.create_cnx_pool()
        self.cnx.get_connection()

        logger.info('******Opening Browser******')
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
        self.browser.close()
        logger.info('Browser closed')
        logger.info('Deleting Song Instances')
        self.cnx.del_test_song_instances()
        logger.info('Closing DB Connection')
        self.cnx.close_connection()
        logger.info('Testing module complete')

    def test_get_617_page(self):
        station_dict=self.cnx.get_station_url_and_type('921')
        self.browser.get(station_dict['url'])
        self.assertTrue('indie617' in self.browser.title, 'Issue geting 617 song history page')

    def test_get_triton_song_section(self):
        station_dict=self.cnx.get_station_url_and_type('921')
        tri_pars = TritonParser()
        song_df=tri_pars.get_triton_df(station_dict['url'])

        self.assertTrue(len(song_df)>0, "Issue parseing page")

    def test_df_timestamp_conversion(self):
        df=Utils.convert_df_milisec_to_timestamp(self.test_song_df)
        song_ts=df.iloc[0,0]
        test_ts=datetime.strptime('2019-12-15 22:21:05','%Y-%m-%d %H:%M:%S')
        self.assertTrue(song_ts==test_ts,'Issue with converting milliscoend to timestamp')

    def test_df_timestamp_filter(self):
        sie=SongInsertEngine(self.cnx)
        df=Utils.convert_df_milisec_to_timestamp(self.test_song_df)
        df=sie.filter_df_by_web_id_time(df,1)
        self.assertTrue(len(df.index)==9, 'Issue with filtering dataframe by timestamp')

    def test_bulk_song_instance_inserts(self):
        dummy=self.cnx.get_last_song_time_by_staion_id(1)
        sie=SongInsertEngine(self.cnx)
        df=Utils.convert_df_milisec_to_timestamp(self.test_song_df)
        df=sie.filter_df_by_web_id_time(df,1)
        sie.process_song_instances(df,1)
        insert_cnt=self.cnx.get_song_instance_count(1)
        self.assertTrue(insert_cnt==9,'Issue inserting song instances')

    def test_negative_scrape_songs_1(self):
        scraper=ScrapeSongs(self.cnx)
        results=scraper.scrape_songs(344)
        self.assertTrue(results=='Web station with id 344 not yet set up for scraping')

    def test_scrape_songs(self):
        scraper=ScrapeSongs(self.cnx)
        results=scraper.scrape_songs(921)
        print(str(results))
        self.assertTrue(results is None, "Issue with scraping songs")






