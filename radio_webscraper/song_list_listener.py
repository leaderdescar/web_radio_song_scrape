from radio_webscraper.dao import DBConnection
from radio_webscraper.parser import Parser
from radio_webscraper.utils import Utils
import logging


class SongListListener(object):
    '''
    classdocs
    '''

    def __init__(self):

        db_config = Utils.get_config()
        self.dao_obj = DBConnection(db_config['user'], 
                                     db_config['password'],
                                     db_config['host'], 
                                     db_config['database'])
        self.dao_obj.create_cnx_pool()
        '''Start up
            Get list of stations and url from DB --method should be in DOA
            
            90 second loop:
                for each station:
                    get latest song played from web -parse passed url station
                    
                    run a query to check if html song id is in DB 
                    if html song id is new:
                        get artist id by artist name
                        if no artist ID
                            insert new artist
                            get new artist id
                        get album id by album name
                        if no album id
                            insert new album
                            get new album name
                        get song id by song name
                        if no song id
                            insert new song
                            get new song id
                        
                        insert new song instance
                        update station
                            
        
        '''

    def get_stations_info_list(self):
        '''
        gets list of stations and url in DB
        '''
        #get connection
        self.dao_obj.get_connection()
        #get station list
        station_list = self.dao_obj.get_station_info()
        self.dao_obj.close_connection()
        return station_list
    
    def listen_to_playlist(self, station_list,db_last_played = '',page_type='url'):
        #listen to web radio play lists and record the latest song in the DB  
        
        for station in station_list:
            station_id = station['web_station_id']
            station_name = station['web_station_name']
            station_url = station['url_text']
            
            if db_last_played == '':
            #last_played_in_db
                self.dao_obj.get_connection()
                db_last_played_id = self.dao_obj.last_played_in_db(station_id)
                self.dao_obj.close_connection()
            
            #parse webpage
            parser = Parser()
            radio_web_palylist = parser.get_webpage(station_url)
            web_current_song = parser.parse_webpage(radio_web_palylist, station_id, db_last_played_id, page_type)
            last_web_song_played_id = web_current_song.html_song_id
            
            if last_web_song_played_id != db_last_played_id:
                #start insert routine
                
                #artist
                self.dao_obj.get_connection()
                artist_results = self.dao_obj.get_artist_id(web_current_song.artist)
                self.dao_obj.close_connection()
                
                if artist_results:
                    web_current_song.artist_id = artist_results
                else:
                    self.dao_obj.get_connection()
                    self.dao_obj.insert_new_artist(web_current_song.artist)
                    web_current_song.artist_id=self.dao_obj.get_artist_id(web_current_song.artist)
                    self.dao_obj.close_connection()
                    
                #album
                self.dao_obj.get_connection()
                album_results = self.dao_obj.get_album_id(web_current_song.album, 
                                                          web_current_song.artist_id)
                self.dao_obj.close_connection()
                
                if album_results:
                    web_current_song.album_id = album_results
                else:
                    self.dao_obj.get_connection()
                    self.dao_obj.insert_new_album(web_current_song.album, 
                                                  web_current_song.artist_id)
                    web_current_song.album_id = self.dao_obj.get_album_id(web_current_song.album, 
                                                                          web_current_song.artist_id)
                    self.dao_obj.close_connection()
                
                #song
                self.dao_obj.get_connection()
                song_results = self.dao_obj.get_song_id(web_current_song.song, 
                                                        web_current_song.artist_id, 
                                                        web_current_song.album_id)
                self.dao_obj.close_connection()
                
                if song_results:
                    song_results=web_current_song.song_id 
                else:
                    self.dao_obj.get_connection()
                    self.dao_obj.get_song_id(web_current_song.song, 
                                                            web_current_song.artist_id, 
                                                            web_current_song.album_id)
                    web_current_song.song_id = self.dao_obj.get_song_id(web_current_song.song, 
                                                                        web_current_song.artist_id, 
                                                                        web_current_song.album_id)
                    self.dao_obj.close_connection()
                    
                #Insert song instance                   
                self.dao_obj.get_connection()
                self.dao_obj.insert_song_instance(web_current_song.song_id, 
                                                  station_id, 
                                                  web_current_song.html_song_id) 
                self.dao_obj.close_connection()  

    

    

        