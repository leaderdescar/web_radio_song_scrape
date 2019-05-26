'''
Created on Jan 21, 2019

@author: papa
'''
import unittest

from radio_webscraper.utils import Utils
from radio_webscraper.dao import DBConnection
import logging


class TestInserts(unittest.TestCase):


    def setUp(self):
        
        Utils.initialize_logging(self)
        
        db_config = Utils.get_config(self)
        self.cnx = DBConnection(db_config['user'], 
                                 db_config['password'],
                                 db_config['host'], 
                                 db_config['database'])
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

        self.cnx.insert_new_artist('test_artist_name')
        new_artist_id = self.cnx.get_artist_id('test_artist_name')
        
        self.assertTrue(new_artist_id, 'Issue with inserting Artist')
        self.artist_id = new_artist_id[0]


    def test2_insert_album(self):
    


        self.cnx.insert_new_album('test_album_name', '1')
        new_album_id=self.cnx.get_album_id('test_album_name', '1')
        
        self.assertTrue(new_album_id, 'Issue with inserting album')
        
        self.album_id = new_album_id[0]

    def test3_insert_song(self):
    
        self.cnx.insert_new_song('test_song', '1', '1')
        new_song_id = self.cnx.get_song_id('test_song', '1', '1')
        
        self.assertTrue(new_song_id, 'issue inserting or selecting song')
        self.song_id = new_song_id  

    def test_web_station_select(self):
        station_info = self.cnx.get_station_info()
        url = station_info[0]['url_text']
        self.assertTrue(url == 'www.player.listenlive.co/35471/en/songhistory', 'Issue return url from DB')
        
'''
    def test_insert_song_instance(self):
        pass
'''

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()