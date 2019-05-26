'''
Created on Dec 9, 2018

@author: papa
'''

class Album(object):
    '''
    classdocs
    '''


    def __init__(self, id, album_name, artist_id):
        '''
        Constructor
        '''
        self.id = id
        self.album_name = album_name
        self.artist_id
        
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self,id):
        self.__id = id
        
    @property
    def album_name(self):
        return self.__album_name
    
    @album_name.setter
    def album_name(self,album_name):
        self.__album_name = album_name
        
    @property
    def artist_id(self):
        return self.__artist_id
    
    @artist_id.setter
    def artist_id(self,artist_id):
        self.__artist_id = artist_id
        

        