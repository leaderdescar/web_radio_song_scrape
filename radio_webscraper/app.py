'''
Created on Jan 1, 2019

@author: papa
'''
from radio_webscraper.doa import DBConnection
from radio_webscraper.parser import Parser
from radio_webscraper.utils import Utils
import logging
from flask import Flask


#Create connection pool
db_config = Utils.get_config()
cnx = DBConnection(db_config['user'], 
                             db_config['password'],
                             db_config['host'], 
                             db_config['database'])
cnx.create_cnx_pool()

    




if __name__ == '__main__':
    #TODO: Change to run app
    
    pass
