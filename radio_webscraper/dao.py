'''
Created on Dec 29, 2018

@author: papa
'''

from radio_webscraper.utils import Utils
import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector import pooling
from mysql.connector import Error
from mysql.connector import errorcode
import logging

class DBConnection(object):
    '''
    classdocs
    '''


    def __init__(self,user,password,host,database):
        '''
        Constructor
        '''
        self.user=user
        self.password=password
        self.host=host
        self.database=database

    def create_cnx_pool (self):
        
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="song_lstn_pool",
                                                                               pool_size=5,
                                                                               pool_reset_session=True,
                                                                               host=self.host,
                                                                               database=self.database, 
                                                                               user=self.user,
                                                                               password=self.password)
            logging.debug("Printing connection pool properties ")
            logging.debug("Connection Pool Name - ", self.connection_pool.pool_name)
            logging.debug("Connection Pool Size - ", self.connection_pool.pool_size)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logging.error( '''Something is wrong with your user name or password''')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logging.error( '''Database does not exist: %s''',self.database)
            else:
                logging.error(err)
        #else:
            #self.current_cursor = self.connection_pool.cursor(buffered=True)
            #return self.connection_pool
            
    def get_connection(self):
        
        #TODO: change over to connection pool
        self.cnx = self.connection_pool.get_connection()
        if self.cnx.is_connected():
            db_Info = self.cnx.get_server_info()
            logging.debug("Connected to MySQL database using connection pool ... MySQL Server version on ",db_Info)
            self.current_cursor = self.cnx.cursor(buffered=True)
            
    def run_test(self):
        query=('''SELECT VERSION ()''')
        
        self.current_cursor.execute(query)
        
        results = self.current_cursor.fetchone()
        # Check if anything at all is returned
        if results:
            return True
        else:
            return False 
        
    def last_played_in_db (self,web_station_id,native_playlist_id):
        '''
        Checks if the current song is already in the DB based on page
        native song id
        '''
        query=('''SELECT native_playlist_id as check_value FROM song_instance_t '''
               +'''WHERE web_station_id = %s''')
        
        self.current_cursor.execute(query,(web_station_id,native_playlist_id))
        
        for (native_playlist_id) in self.current_cursor:
            return native_playlist_id

    
    def insert_song_instance(self,song_id,web_station_id,native_playlist_id):
            
            query=('''INSERT INTO song_instance_t (song_id,web_station_id, native_playlist_id) '''
                   +'''VALUES (%s, %s, %s)''')
            
            self.current_cursor.execute(query,(song_id,web_station_id,native_playlist_id))
            self.cnx.commit()
    
    def get_artist_id (self,artist_name):
        
        query = ('''SELECT artist_id FROM artist_t WHERE artist_name = %s''')

        self.current_cursor.execute(query,(artist_name,))
        
        for(artist_id) in self.current_cursor:
            return artist_id
        
    def insert_new_artist(self,artist_name):
        
        query = ('''INSERT INTO artist_t (artist_name)'''
                 +'''VALUES (%s)''')
        
        self.current_cursor.execute(query,(artist_name,))
        self.cnx.commit()
        
    def get_album_id (self,album_name, artist_id):
        
        query = ('''SELECT album_id FROM album_t '''
                 +'''WHERE album_name = %s '''
                 +'''AND artist_id = %s''')
        self.current_cursor.execute(query,(album_name, artist_id))
        
        for (album_id) in self.current_cursor:
            return album_id
        
    def insert_new_album(self,album_name, artist_id):
        
        query = ('''INSERT INTO album_t (album_name, artist_id) '''
                 +'''VALUES (%s,%s)''')
        
        self.current_cursor.execute(query,(album_name, artist_id))
        self.cnx.commit()
        
    def get_song_id (self,song_name, artist_id,album_id):
        '''
        Returns song id for passed parameters
        Params: song_name, artist_id, album_id
        '''
        query = ('''SELECT song_id  FROM song_t '''
                 +'''WHERE song_name = %s '''
                 +'''AND artist_id = %s '''
                 +'''AND album_id = %s ''')
        
        self.current_cursor.execute(query,(song_name, artist_id,album_id))
        
        for (song_id) in self.current_cursor:
            return song_id
        
    def insert_new_song(self,song_name, artist_id,album_id):
        '''
        Inserts new song into song table
        params: song_name, artist_id, album_id
        '''
        
        query = ('''INSERT INTO song_t (song_name, artist_id,album_id) ''' 
                 +'''VALUES (%s, %s, %s)''')
        
        self.current_cursor.execute(query,(song_name, artist_id,album_id))
        self.cnx.commit()
        
    def get_station_info(self):
        '''
        returns list of station dictionaries
        '''
        station_list=[]
        query = ('''SELECT web_station_id,web_station_name,web_station_playlist_url_txt FROM web_station_t ORDER BY web_station_id'''
                 )
        
        self.current_cursor.execute(query)
        
        for (web_station_id,web_station_name,web_station_playlist_url_txt) in self.current_cursor:
            station_info = {'web_station_id':web_station_id, 'web_station_name':web_station_name, 'url_text':web_station_playlist_url_txt }
            station_list.append(station_info)
        return station_list
        
    def list_stations (self):
        
        query = ('''SELECT web_station_name FROM web_station_t''')
        
        station_names = []
        self.current_cursor.execute(query)
        
        for (web_station_name) in self.current_cursor:
            station_names.append(web_station_name,)
        
        return station_names
    
    def close_connection(self):
        #self.cnx.close()
        if(self.cnx.is_connected()):
            self.current_cursor.close()
            self.cnx.close()
        
    def del_song_id (self,song_id):
        query =('DELETE FROM song_t WHERE song_id = %s')
        self.current_cursor.execute(query,(song_id,))
        self.cnx.commit()
  
          
    def del_artist_id(self,artist_id):
        query =('DELETE FROM artist_t WHERE artist_id = %s')
        self.current_cursor.execute(query,(artist_id,))
        self.cnx.commit()

        
    def del_album_id(self,album_id):      
        query =('''DELETE FROM album_t WHERE album_id = %s''')
        self.current_cursor.execute(query,(album_id,))
        self.cnx.commit()

            
        
        
        
        
        
        
            
        
        
        