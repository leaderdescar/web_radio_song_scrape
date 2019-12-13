
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import datetime
from radio_webscraper.model.songinfo import SongListInstance
from radio_webscraper.utils import Utils
import logging
import pathlib



class OldParser(object):
    '''
    Parse the play list page, determines if song currently playing is new.
    if it is, then tests for song title. If there is a song tile, sets
    '''


    def __init__(self):
        '''
        Constructor
        '''
        cur_dir = str(pathlib.Path.cwd())
        ##cur_dir =cur_dir.replace('''/radio_webscraper''', '')

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.browser = webdriver.Chrome(chrome_options=options)

        
    def get_webpage(self,url):
        try:
            web_page = self.browser.get(url)
            return web_page
        except Exception as e:
            logging.info(Utils.return_timestamp(self) + e)
           
    def parse_webpage(self,web_page,web_station_id,last_html_id,page_type):
        
        #placce holder for future logic
        if web_station_id is None:
            pass
        
        if page_type == 'text':
            soup_page = BeautifulSoup(web_page,'html.parser')
        else:
            soup_page = BeautifulSoup(web_page.page_source,'html.parser')
             
        soup2 = soup_page.find(class_='songs tracks')
        soup3 =soup2.find(class_='info')
        
        #traverse song playlist
        soup_title = soup3.find(class_='title')

        #get song at top of playlist
        if soup_title is None:
            print(Utils.return_timestamp(self) + ' No Song Title, retrying later')
        else:
            
            title_name = soup_title.find('a')
            if title_name is None:
                title_name = soup_title.get_text()
            else:
                title_name = title_name.get_text()
                
            soup4 = soup_page.find(class_= 'timestamp')
            html_song_id = soup4.find(class_='cutieTime')['data-timestamp']
                
            current_song = SongListInstance(title_name.strip(),html_song_id)
             
            #check if new song and get artist
            if html_song_id is last_html_id:
                logging.info(Utils.return_timestamp(self) + 'Previous song still playing')
                
            else:
                soup_artist = soup3.find(class_='artist')
                
                if soup_artist is None:
                    logging.info(Utils.return_timestamp(self) + ' No artist found, saving song without artist')
                else:
                    artist_name = soup_artist.find('a')
                    if artist_name is None:
                        artist_name = soup_artist.get_text()
                    else:
                        artist_name = artist_name.get_text()
                        
                    current_song.artist = artist_name.strip()
                
                #get album
                soup_album = soup3.find(class_='album')
                
                if soup_album is None:
                    logging.info(Utils.return_timestamp(self) + ' No Album Found, saving song without Album')
                else:
                    album_name = soup_album.find('a')
                    if album_name is None:
                        album_name = soup_album.get_text()
                    else:
                        album_name = album_name.get_text()
                    
                    current_song.album = album_name.strip()
                    
        
        return current_song

                    

                
            
            

        
    