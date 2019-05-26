'''
Created on Dec 9, 2018

@author: papa
'''


class Artist(object):
    '''
    classdocs
    '''


    def __init__(self, id, artist_name):
        '''
        Constructor
        '''
        self.id = id
        self.artist_name = artist_name
        
    @property
    def id (self):
        return self.__id
    
    @id.setter
    def id (self,id):
        self.__id=id
        
    @property
    def artist_name(self):
        return self.__artist_name
    
    @artist_name.setter
    def artist_name(self, artist_name):
        self.__artist_name=artist_name
        
    