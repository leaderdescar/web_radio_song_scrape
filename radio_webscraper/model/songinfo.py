'''
Created on Dec 23, 2018

@author: papa
'''

class SongListInstance(object):
    '''
    classdocs
    '''
    _last_html_id = None

    def __init__(self,song,html_song_id):
        '''
        Constructor
        '''
        self.song = song
        self.html_song_id = html_song_id
        self.artist = ''
        self.album = ''
        self.artist_id = ''
        self.album_id = ''
        self.song_id = ''
        
            
    @property
    def song(self):
        return self.__song
    
    @song.setter
    def song(self,song):
        self.__song = song
        
    @property
    def artist(self):
        return self.__artist
    
    @artist.setter
    def artist(self,artist):
        self.__artist = artist
        
    @property
    def album(self,album):
        return self.__album
    
    @album.setter
    def album(self,album):
        self.__album = album
        

    
        
