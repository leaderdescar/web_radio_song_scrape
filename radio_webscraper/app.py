'''
Created on Jan 1, 2019

@author: papa
'''

import logging
import logging.config
from flask import Flask
from flask import request
from flask import make_response
from flask import abort
import sqlalchemy
import sys
from utils import Utils
from db_interface.dao import DBConnection
from processor.scrape_songs_engine import ScrapeSongs


#Setup

app=Flask(__name__.split('.')[0])

logging.config.fileConfig(fname='config/test_logging.conf', disable_existing_loggers=False)

logger=logging.getLogger(__name__)

try:
    logger.info('*******Starting App********')
    db_config = Utils.get_config()
    cnx=DBConnection(db_config['user'],
                                 db_config['password'],
                                 db_config['host'],
                                 db_config['database'],
                                 db_config['schema'])
    cnx.create_cnx_pool()

except sqlalchemy.exc.SQLAlchemyError as error:
    logger.error(f'Issue with connecting to db and creating connection pool: {error}')


@app.route('/scrape_songs_by_station_id/<int:id>',methods=['GET'])
def scrape_songs_by_station_id(id):
    web_id = request.args.get('id')

    cnx.get_connection()
    try:
        logger.info(f'Scraping songs for station id {id}')
        scraper = ScrapeSongs(cnx)
        results = scraper.scrape_songs(id)
        if results is not None:
            logger.warn(results)
            return results
            abort(504)
        insert_cnt = cnx.get_song_instance_count(id)

    except:
        e = sys.exc_info()[0]
        logger.error(f'Error in calling scrape songs by station id endpoint: {e}', exc_info=True)
        abort(400)


    cnx.close_connection()

    return f'Sucessfully parsedand inserted {insert_cnt} songs to DB'


    




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
