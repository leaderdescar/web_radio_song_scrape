'''
Created on Dec 29, 2018

@author: papa
'''

from radio_webscraper.utils import Utils
import logging
from sqlalchemy.engine import create_engine
import pg8000
import datetime



class DBConnection(object):
    '''
    classdocs
    '''


    def __init__(self,user,password,host,database,schema):
        '''
        Constructor
        '''
        self.user=user
        self.password=password
        self.host=host
        self.database=database
        self.schema=schema
        self.last_playlist_song_timestamp=''



    def create_cnx_pool (self):
        #no need for try and catch, already built into sqlalchemy
        db_url=("postgresql+pg8000://%s:%s@%s:5432/%s"%(self.user,
                                                self.password,
                                                self.host,
                                                self.database))

        self.connection_pool=create_engine(db_url,max_overflow=0)
            
    def get_connection(self):
        self.cnx=self.connection_pool.connect()
            
    def run_test(self):
        query=('''SELECT VERSION ()''')

        results=self.cnx.execute(query)
        # Check if anything at all is returned
        if results:
            return True
        else:
            return False 
        
    def get_last_song_time_by_staion_id (self,web_station_id):
        '''
        Checks if the current song is already in the DB based on page's
         song timestamp
        '''
        query=f"SELECT MAX(playlist_song_timestamp) as check_value FROM {self.schema}.song_instance_t "\
               f"WHERE web_station_id = {web_station_id}"
        
        self.last_playlist_song_timestamp=self.cnx.execute(query).scalar()
        if self.last_playlist_song_timestamp is None:
            self.last_playlist_song_timestamp=datetime.datetime.strptime('2017-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')

        return self.last_playlist_song_timestamp

    
    def insert_song_instance(self,song_id,web_station_id,playlist_song_timestamp):
            
            query=f"INSERT INTO {self.schema}.song_instance_t (song_id,web_station_id, playlist_song_timestamp) "\
                   f"VALUES ({song_id}, {web_station_id}, '{playlist_song_timestamp}')"
            
            self.cnx.execute(query)
            
    
    def get_artist_id (self,artist_name):      
        query = f"SELECT artist_id FROM {self.schema}.artist_t WHERE artist_name = %s"
        artist_id = self.cnx.execute(query,(artist_name,)).scalar()
        return artist_id
        
    def insert_new_artist(self,artist_name):
        query=f"INSERT INTO {self.schema}.artist_t (artist_name) VALUES (%s) RETURNING artist_id"
        new_artist_id=self.cnx.execute(query,(artist_name,)).scalar()
        return new_artist_id
        
    def get_album_id (self,album_name, artist_id):
        query =  f"SELECT album_id FROM {self.schema}.album_t "\
                 f"WHERE album_name = %s "\
                 f"AND artist_id = %s"
        album_id = self.cnx.execute(query,(album_name,artist_id)).scalar() 
        return album_id
        
    def insert_new_album(self,album_name, artist_id):
        query = f"INSERT INTO {self.schema}.album_t (album_name, artist_id)"\
                f"VALUES (%s,%s) "\
                "RETURNING album_id"
        
        new_album_id=self.cnx.execute(query,(album_name,artist_id)).scalar()
        return new_album_id
        
        
    def get_song_id (self,song_name, artist_id,album_id):
        '''
        Returns song id for passed parameters
        Params: song_name, artist_id, album_id
        '''
        query = f"SELECT song_id  FROM {self.schema}.song_t "\
                 f"WHERE song_name = %s "\
                 f"AND artist_id = %s "\
                 f"AND album_id = %s"
        
        song_id = self.cnx.execute(query,(song_name,artist_id,album_id)).scalar()
        return song_id
        
    def insert_new_song(self,song_name, artist_id,album_id):
        '''
        Inserts new song into song table
        params: song_name, artist_id, album_id
        '''
        query = f"INSERT INTO {self.schema}.song_t (song_name, artist_id,album_id) "\
                f"VALUES (%s, %s, %s)"\
                "RETURNING song_id"
        
        new_song_id=self.cnx.execute(query,(song_name,artist_id,album_id)).scalar()
        return new_song_id
        
    def get_station_url_and_type (self,web_station_id):
        result_dict={}
        query = f"SELECT web_station_url, web_station_type_code FROM {self.schema}.web_station_t "\
            f"WHERE web_station_id = %s"
        results=self.cnx.execute(query,(web_station_id,))
        for url,type_code in results:
            result_dict={'url':url,'type_code':type_code}
        return result_dict      

    def get_info_all_stations(self):
        '''
        returns list of station dictionaries
        '''
        station_list=[]
        query = "SELECT web_station_id,web_station_name,web_station_url, web_station_type_code"\
                f"FROM {self.schema}.web_station_t ORDER BY web_station_id"
        
        results=self.cnx.execute(query)
        
        #this likley needs to be re-worked, maybe bind table schema
        for (web_station_id,web_station_name,web_station_url,web_station_type_code) in results:
            station_info = {'web_station_id':web_station_id, 'web_station_name':web_station_name, 'url_text':web_station_url, 'web_station_type_code':web_station_type_code}
            station_list.append(station_info)
        return station_list
        
    def list_stations_by_name (self):
        query = f"SELECT web_station_name FROM {self.schema}.web_station_t"
        station_names = []
        results=self.cnx.execute(query)
        
        #TODO rework possible
        for (web_station_name) in results:
            station_names.append(web_station_name,)
        return station_names

    def close_connection(self):
        if(self.cnx.closed is False):
            self.cnx.close()


    def del_song_id (self,song_id):
        query =f"DELETE FROM {self.schema}.song_t WHERE song_id = {song_id}"
        self.cnx.execute(query)
        
          
    def del_artist_id(self,artist_id):
        query =f"DELETE FROM {self.schema}.artist_t WHERE artist_id = {artist_id}"
        self.cnx.execute(query)
        

    def del_album_id(self,album_id):      
        query =f"DELETE FROM {self.schema}.album_t WHERE album_id = {album_id}"
        self.cnx.execute(query)

    def del_test_song_instances(self):
        query=f'DELETE FROM {self.schema}.song_instance_t WHERE web_station_id = 1'
        self.cnx.execute(query)

    def get_test_song_instance_cnt(self):
        query=f'SELECT Count(*) as cnt FROM {self.schema}.song_instance_t WHERE web_station_id = 1 '
        song_cnt=self.cnx.execute(query).scalar()
        return song_cnt
    
    def get_song_instance_count(self,web_station_id):

        query=f'SELECT Count(*) as cnt FROM {self.schema}.song_instance_t WHERE web_station_id = {web_station_id} '\
            f'AND playlist_song_timestamp > %s'
        song_cnt=self.cnx.execute(query,(str(self.last_playlist_song_timestamp),)).scalar()
        return song_cnt


