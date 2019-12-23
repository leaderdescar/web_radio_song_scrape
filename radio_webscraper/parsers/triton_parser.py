'''
Created on Dec 15, 2019

Parse for Triton based web sites
Returns songs in a dataframe

@author: papa
'''
import logging
import pandas as pd
from bs4 import BeautifulSoup
from radio_webscraper.utils import Utils
from radio_webscraper.browser import browser_engine as be


class TritonParser(object):

    def __init__(self):

        self.browser = be.BrowserEngine().get_browser()

    def get_triton_df(self,url):
        '''
        Main method of class
        takes in a url, gets the song block from the page
        converts the song block into a list dictionaries
        then to a data frame.

        Returns a data frame
        '''

        source_page=self.get_triton_page(url)
        songs_block=self.get_triton_songs_block(source_page)
        song_dict_list=self.get_triton_songs_list(songs_block)
        song_df=self.convert_triton_list_to_df(song_dict_list)

        return song_df


    def get_triton_page(self,url):
        #Returns html source page

        self.browser.get(url)
        source_page=self.browser.page_source
        self.browser.close()
        return source_page
    
    def get_triton_songs_block(self,source_page):
        #Returns rasw song block from triton page

        soup=BeautifulSoup(source_page,'html.parser')
        main_section=soup.find(id='wrapper')
        songs_section=main_section.find('script',type='text/javascript')
        songs_block=songs_section.get_text()

        #isolate song data 
        songs_block=songs_block.split('[',1)[1]
        songs_block=songs_block.rsplit(']',1)[0]

        return songs_block
    
    def get_triton_songs_list(self,songs_block):
        #Retruns list of dictionaries of songs

        #convert song block string to list of dictionaries
        song_dict_list=[]
        song_str_list=songs_block.split('},')
        for song_str in song_str_list:
            if '}' not in song_str:
                song_str=song_str+'}'
            
            song_dict=eval(song_str)

            #remove unwanted keys
            song_dict = self.remove_triton_song_keys(song_dict)

            song_dict_list.append(song_dict)
        
        return song_dict_list

    def remove_triton_song_keys(self,song_dict):
        #Returns song dictionary with keys removed

        #remove unwanted keys
        song_dict.pop("trackId", None)
        song_dict.pop("artistId", None)
        song_dict.pop("albumId", None)
        song_dict.pop("npe_id", None)

        return song_dict

    def convert_triton_list_to_df(self, song_dict_list):
        #returns a dataframe

        song_df=pd.DataFrame(song_dict_list)
        song_df.rename(columns = {'title':'song_name', 'artist':'artist_name', 
                                      'album':'album_name'}, inplace = True)
        
        return song_df





    


