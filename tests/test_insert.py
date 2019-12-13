'''
Created on Jan 21, 2019

@author: papa
'''
import unittest

from radio_webscraper.utils import Utils
from radio_webscraper.dao import DBConnection
import logging
import datetime


class TestInserts(unittest.TestCase):


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
        
        self.artist_id = ''
        self.album_id = ''
        self.song_id = ''


    def tearDown(self):
        
        if isinstance(self.song_id, int):
            self.cnx.del_song_id(self.song_id)        
        
        if isinstance(self.album_id, int):
            self.cnx.del_album_id(self.album_id)
        
        if isinstance(self.artist_id, int):
            self.cnx.del_artist_id(self.artist_id)

        self.cnx.close_connection()

    def test1_insert_artist(self):
        new_artist_id=self.cnx.insert_new_artist('test_artist_name')
        inserted_artist_id = self.cnx.get_artist_id('test_artist_name')
        
        self.assertTrue(new_artist_id == inserted_artist_id, 'Issue with inserting Artist')
        self.artist_id = new_artist_id


    def test2_insert_album(self):
        new_album_id=self.cnx.insert_new_album('test_album_name', '1')
        inserted_album_id=self.cnx.get_album_id('test_album_name', '1')
        
        self.assertTrue(new_album_id==inserted_album_id, 'Issue with inserting album')
        self.album_id = new_album_id

    def test3_insert_song(self):
        new_song_id=self.cnx.insert_new_song('test_song', '1', '1')
        inserted_song_id=self.cnx.get_song_id('test_song', '1', '1')
        
        self.assertTrue(new_song_id==inserted_song_id, 'issue inserting or selecting song')
        self.song_id = new_song_id  

    def test4_instert_song_instance(self):
        current_timestamp=str(datetime.datetime.fromtimestamp(1574946234000/1000.0))
        print('Current Timestamp:'+ current_timestamp)
        self.cnx.insert_song_instance('1','921',current_timestamp)

        max_timestamp=str(self.cnx.last_song_by_staion_id_saved(921))
        print('Max Timestamp: '+max_timestamp)
      
        self.assertTrue(current_timestamp==max_timestamp, 'issue inserting song instance')

    def test_get_station_url(self):
        url = self.cnx.get_station_url(921)
        self.assertTrue(url == 'http://player.listenlive.co/35471/en/songhistory', 'Issue return url from DB')
        
'''
    def test_insert_song_instance(self):
        pass
'''

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()