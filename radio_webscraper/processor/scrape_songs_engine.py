'''
Created on Dec 23, 2019

Main module to call other modules
to get web page, parse page, load songs
into a data frame, filter songs by timestamp
and insert songs into database

@author: papa
'''
import logging
import pandas as pd
from utils import Utils
from db_interface.dao import DBConnection
from parsers.triton_parser import TritonParser
from processor.song_insert_engine import SongInsertEngine




class ScrapeSongs(object):

    def __init__(self,cnx):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.cnx = cnx

        self.insert_engine = SongInsertEngine(cnx)

    
    def scrape_songs(self,web_station_id):
        start_time = Utils.return_timestamp()
        self.logger.info(f'Started parse of web station history at {start_time}')
        web_station_dict = self.cnx.get_station_url_and_type(web_station_id)
        #self.cnx.close_connection()
        if len(web_station_dict) > 0:
            song_df = self.parse_station_page(str(web_station_dict['url']),str(web_station_dict['type_code']))
            
            if isinstance(song_df, pd.DataFrame):
                self.insert_songs(song_df, web_station_id)
            else:
                return f'No parser available for web_station_id {web_station_id}'
        else:
            return f'Web station with id {web_station_id} not yet set up for scraping'
        end_time = Utils.return_timestamp()
        self.logger.info(f'Parse and insert completed at {end_time}')

        return None


    def parse_station_page(self,url,type_code):
        
        if type_code == 'tri':
            self.logger.info('Using Triton Parser')
            parser=TritonParser()
            df=parser.get_triton_df(url)
            return df
        else:
            return 'N/A'

    def insert_songs(self,song_df,web_station_id):
        df_converted=Utils.convert_df_milisec_to_timestamp(song_df)
        df_filtered=self.insert_engine.filter_df_by_web_id_time(df_converted,web_station_id)
        self.insert_engine.process_song_instances(df_filtered,web_station_id)


