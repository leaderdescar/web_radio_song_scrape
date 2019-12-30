'''
Created on Dec 23, 2019

@author: papa
'''
from utils import Utils
from db_interface.dao import DBConnection
import pandas as pd
import logging





class SongInsertEngine(object):
    '''
    classdocs
    '''


    def __init__(self,cnx):
        '''
        Constructor
        '''
        self.logger=logging.getLogger(self.__class__.__name__)
        
        db_config = Utils.get_config()

        self.cnx = cnx
        
        self.artist_id = ''
        self.album_id = ''
        self.song_id = ''

    def process_song_instances(self,song_df,web_station_id):

        #Iterate over each df row, insert in
        #Df is already filtered for latest played songs

        self.logger.debug(str(song_df))

        for index, row in song_df.iterrows():
            if pd.notnull(row.song_name):
                self.artist_id = self.process_artist(row.artist_name)
                self.album_id = self.process_album(row.album_name, self.artist_id)
                self.song_id = self.process_song( row.song_name, self.artist_id, self.album_id)
                self.cnx.insert_song_instance( self.song_id, web_station_id, row.timestamp)

                self.artist_id=''
                self.album_id=''
                self.song_id=''





    def filter_df_by_web_id_time(self,song_df,web_station_id):
        #filter the datframe to only keep songs greater
        #than the max timestamp for a webstation in
        #song instances

        #miliseconds need to be converted in df to timestamp
        #should be done in each parse acording to source site needs
        max_timestamp=self.cnx.get_last_song_time_by_staion_id(web_station_id)
        filtered_song_df = song_df[song_df['timestamp'] > max_timestamp]
        

        return filtered_song_df


    def process_artist(self,artist_name):

        if pd.isnull(artist_name):
            artist_name='Unknown Artist'

        artist_id_results=self.cnx.get_artist_id(artist_name)

        if artist_id_results:
            artist_id=artist_id_results
        else:
            artist_id=self.cnx.insert_new_artist(artist_name)
        return artist_id


    def process_album(self,album_name,artist_id):

        if pd.isnull(album_name):
            album_name='Unknown Album Name'

        album_id_results=self.cnx.get_album_id(album_name,artist_id)

        if album_id_results:
            album_id=album_id_results
        else:
            album_id=self.cnx.insert_new_album(album_name,artist_id)
        return album_id

    def process_song(self,song_name,artist_id, album_id):

        song_id_results=self.cnx.get_song_id(song_name, artist_id, album_id)

        if song_id_results:
            song_id=song_id_results
        else:
            song_id=self.cnx.insert_new_song(song_name, artist_id, album_id)
        return song_id






