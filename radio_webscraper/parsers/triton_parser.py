'''
Created on Dec 15, 2019

Parse for Triton based web sites

@author: papa
'''
import logging
from bs4 import BeautifulSoup
from radio_webscraper.utils import Utils
from radio_webscraper.dao import DBConnection
from radio_webscraper.browser import browser_engine as be


class TritonParser(object):

    def __init__(self):

        self.browser = be.BrowserEngine().get_browser()

    def get_triton_page(self,url):

        self.browser.get(url)
        source_page=self.browser.page_source
        return source_page
    
    def get_songs_list(self,source_page):

        soup=BeautifulSoup(source_page,'html.parser')
        main_section=soup.find(id='wrapper')
        songs_section=main_section.find('script',type='text/javascript')
        songs_block=songs_section.get_text()

        #isolate song data 
        songs_block=songs_block.split('[',1)[1]
        songs_block=songs_block.rsplit(']',1)[0]
        #convert to list of dictionaries
        song_dict_list=[]
        song_str_list=songs_block.split('},')
        for song_str in song_str_list:
            if '}' not in song_str:
                song_str=song_str+'}'
            
            song_dict=eval(song_str)

            #remove unwanted keys
            song_dict.pop("trackId", None)
            song_dict.pop("artistId", None)
            song_dict.pop("albumId", None)
            song_dict.pop("npe_id", None)

            song_dict_list.append(song_dict)

        return song_dict_list



