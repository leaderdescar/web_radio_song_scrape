'''
Created on Dec 28, 2018

@author: papa
'''
import time
import datetime
import pathlib
import json
import logging
import pandas as pd


class Utils(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    @staticmethod
    def return_timestamp():
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        return st
    
    @staticmethod
    def get_config():
        cur_dir = str(pathlib.Path.cwd())
        path_parts = cur_dir.partition('/RadioWebScraper')
        cur_dir = path_parts[0]
        with open(cur_dir +'/config/config.json', 'r') as f:
            config = json.load(f)
        
        db_config_dic = {}
        db_config_dic['user'] = config['DEFAULT']['user']
        db_config_dic['password'] = config['DEFAULT']['password']
        db_config_dic['host'] = config['DEFAULT']['host']
        db_config_dic['database'] = config['DEFAULT']['database']
        db_config_dic['schema'] = config['DEFAULT']['schema']
        
        return db_config_dic

    @staticmethod
    def initialize_logging():
        
        #TODO: change to config based on environment
        logger = logging.getLogger(__name__)
        
        # Create handlers
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler('rws_log_file.log')
        c_handler.setLevel(logging.DEBUG)
        f_handler.setLevel(logging.ERROR)
        
        # Create formatters and add it to handlers
        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)
        
        # Add handlers to the logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)
        
    @staticmethod
    def convert_df_milisec_to_timestamp(df):

        df['timestamp']=pd.to_datetime(df['timestamp'],unit='ms')
        return df
        