'''
Created on Dec 9, 2018

@author: papa
'''

class Song(object):
    '''
    classdocs
    '''


    def __init__(self, id, song_title, album_id, artist_id):
        '''
        Constructor
        '''
        self.id =id
        self.song_title = song_title
        self.album_id = album_id
        self.artist_id = artist_id
        
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self,id):
        self.__id = id
        
    @property
    def song_title(self):
        return self.__song_title
    
    @song_title.setter
    def song_title(self,song_title):
        self.__song_title = song_title
        
    @property
    def album_id(self):
        return self.__album_id
    
    @album_id.setter
    def album_id(self,album_id):
        self.__album_id = album_id
        
    @property
    def artist_id(self):
        return self.__artist_id
    
    @artist_id.setter
    def artist_id(self,artist_id):
        self.__artist_id = artist_id
        