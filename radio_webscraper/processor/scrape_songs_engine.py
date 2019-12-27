'''
Created on Dec 23, 2019

Main module to call other modules
to get web page, parse page, load songs
into a data frame, filter songs by timestamp
and insert songs into database

@author: papa
'''
import logging
from radio_webscraper.utils import Utils
from radio_webscraper.db_interface.dao import DBConnection
from radio_webscraper.parsers.triton_parser import TritonParser
from radio_webscraper.processor.song_insert_engine import SongInsertEngine
from datetime import datetime
import pandas as pd



class ScrapeSongs(object):

    def __init__(self):

        Utils.initialize_logging()
        
        db_config = Utils.get_config()
        self.cnx = DBConnection(db_config['user'], 
                                 db_config['password'],
                                 db_config['host'], 
                                 db_config['database'],
                                 db_config['schema'])
        self.cnx.create_cnx_pool()
        self.cnx.get_connection()

        self.insert_engine=SongInsertEngine()

    
    def scrape_songs(self,web_station_id):
        start_time=Utils.return_timestamp()
        print(str(start_time))
        web_station_dict=self.cnx.get_station_url_and_type(web_station_id)
        self.cnx.close_connection()
        print('Type Code: '+ web_station_dict['type_code'])
        if len(web_station_dict) > 0:
            song_df=self.parse_station_page(str(web_station_dict['url']),str(web_station_dict['type_code']))
            
            if isinstance(song_df,pd.DataFrame):
                self.insert_songs(song_df,web_station_id)
            else:
                return f'No parser available for web_station_id {web_station_id}'
        else:
            return f'Web station with id {web_station_id} not yet set up for scraping'


    def parse_station_page(self,url,type_code):
        print(type_code)
        if type_code == 'tri':
            parser=TritonParser()
            df=parser.get_triton_df(url)
            return df
        else:
            return 'N/A'

    def insert_songs(self,song_df,web_station_id):
        sie=SongInsertEngine()
        df_converted=Utils.convert_df_milisec_to_timestamp(song_df)
        df_filtered=sie.filter_df_by_web_id_time(df_converted,web_station_id)
        sie.process_song_instances(df_filtered,web_station_id)


