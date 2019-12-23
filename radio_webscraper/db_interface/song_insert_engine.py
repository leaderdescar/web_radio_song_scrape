'''
Created on Dec 23, 2019

@author: papa
'''
from radio_webscraper.utils import Utils
from radio_webscraper.db_interface.dao import DBConnection





class SongInsertEngine(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        Utils.initialize_logging()
        
        db_config = Utils.get_config()

        self.cnx = DBConnection(db_config['user'], 
                                 db_config['password'],
                                 db_config['host'], 
                                 db_config['database'],
                                 db_config['schema'])
        self.cnx.create_cnx_pool()
        
        
        self.artist_id = ''
        self.album_id = ''
        self.song_id = ''

    def process_song_instances(self,song_df,web_station_id):

        #Iterate over each df row, insert in
        #Df is already filtered for latest played songs

        self.cnx.get_connection()

        for row in song_df.head().itertuples():
            self.artist_id=self.process_artist(row.artist_name)
            self.album_id=self.process_album(row.album_name,self.artist_id)
            self.song_id=self.process_song(row.song_name,self.artist_id,self.album_id)
            self.cnx.insert_song_instance(self.song_id,web_station_id,row.timestamp)

        self.cnx.close_connection()

        self.artist_id=''
        self.album_id=''
        self.song_id=''

    def filter_df_by_web_id_time(self,song_df,web_station_id):
        #filter the datframe to only keep songs greater
        #than the max timestamp for a webstation in
        #song instances

        max_timestamp=self.cnx.last_song_by_staion_id_saved(web_station_id)
        filtered_song_df = song_df > (max_timestamp.timestamp()*1000)
        return filtered_song_df


    def process_artist(self,artist_name):

        artist_id_results=self.cnx.get_artist_id(artist_name)

        if artist_id_results:
            artist_id=artist_id_results
        else:
            artist_id=self.cnx.insert_new_artist(artist_name)
        return artist_id


    def process_album(self,album_name,artist_id):

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






