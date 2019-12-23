'''
Created on Jan 5, 2019

@author: papa
'''
import unittest
import json
import pathlib
from radio_webscraper.utils import Utils
from radio_webscraper.db_interface.dao import DBConnection



class TestDB(unittest.TestCase):
        
    
    def test_config_file(self):
        
        cur_dir = str(pathlib.Path.cwd())
        if '/tests' in cur_dir:
            cur_dir=cur_dir.replace('''/tests''', '')
            
        with open(cur_dir +'/config/config.json', 'r') as f:
            config = json.load(f)
            
        self.assertEqual(config['DEFAULT']['host'], '192.168.86.39', 'config file is not correct')
    
    def test_db_config_util(self):
        db_config = Utils.get_config()
        self.assertEqual(db_config['host'], '192.168.86.39', 'get_config method is incorrect')
        
    def test_db_connection(self):
        db_config = Utils.get_config()
        cnx = DBConnection(db_config['user'], 
                                 db_config['password'],
                                 db_config['host'], 
                                 db_config['database'],
                                 db_config['schema'])
        cnx.create_cnx_pool()
        cnx.get_connection()
        result = cnx.run_test()
        self.assertTrue(result, 'Issue with connection')
        cnx.close_connection()            

if __name__ == "__main__":
    unittest.main()