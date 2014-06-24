#                                                             
#          # ###        /                             ###     
#        /  /###  /   #/                               ###    
#       /  /  ###/    ##                                ##    
#      /  ##   ##     ##                                ##    
#     /  ###          ##                                ##    
#    ##   ##          ##  /##      /###   ##   ####     ##    
#    ##   ##   ###    ## / ###    / ###  / ##    ###  / ##    
#    ##   ##  /###  / ##/   ###  /   ###/  ##     ###/  ##    
#    ##   ## /  ###/  ##     ## ##    ##   ##      ##   ##    
#    ##   ##/    ##   ##     ## ##    ##   ##      ##   ##    
#     ##  ##     #    ##     ## ##    ##   ##      ##   ##    
#      ## #      /    ##     ## ##    ##   ##      ##   ##    
#       ###     /     ##     ## ##    ##   ##      /#   ##    
#        ######/      ##     ##  ######     ######/ ##  ### / 
#          ###         ##    ##   ####       #####   ##  ##/  
#                            /                                
#                           /                                 
#                          /                                  
#                         /                                   
#
#  Haunting Three D Radio's Graveyard Slots
#  Copyright 2014 Michael Marner <michael@20papercups.net>
#  Release under MIT Licence

from Song import Song
import psycopg2
import psycopg2.extras


##
# Abstraction around the music library database
class MusicLibrary:

    ##
    # Constructor.
    # 
    # @param databaseConnection the Psycopg2 object connected to the music database
    def __init__(self, databaseConnection):
        self.db = databaseConnection

    ##
    # Sets the list of names for valid Australian artists.
    #
    # The content of the music database is not at all consistent here. Some use
    # CPA, Australian, c.p.a., etc
    #
    # Here we allow the valid names to be set, so we can add to them from a config file.
    #
    # @param names the list of names to use for Australian artists
    #
    def setAustralianNames(self, names):
        self.ausNames = names


    ##
    # Returns a random demo from the library.
    #
    def getRandomDemo(self):
        cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM cd WHERE demo = '2' ORDER BY RANDOM() LIMIT 1")
        cd = cur.fetchone()
        cur.execute("SELECT * from cdtrack WHERE cdid = %s ORDER BY RANDOM() LIMIT 1;", (cd['id'],))
        track = cur.fetchone()
        return Song(cd, track)


    ##
    # Returns a random local song from the library.
    #
    def getRandomLocal(self):
        cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM cd WHERE local = '2' ORDER BY RANDOM() LIMIT 1")
        cd = cur.fetchone()
        cur.execute("SELECT * from cdtrack WHERE cdid = %s ORDER BY RANDOM() LIMIT 1;", (cd['id'],))
        track = cur.fetchone()
        return Song(cd, track)

    ##
    # Returns a random Australian song from the library.
    #
    def getRandomAustralian(self): 
        cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM cd WHERE cpa = ANY(%s) ORDER BY RANDOM() LIMIT 1", (self.ausNames,))
        cd = cur.fetchone()
        cur.execute("SELECT * from cdtrack WHERE cdid = %s ORDER BY RANDOM() LIMIT 1;", (cd['id'],))
        track = cur.fetchone()
        return Song(cd, track)

    ##
    # Returns a random song from the library.
    #
    # Note that although we have the quota specific methods, this method is totally random, so
    # it's possible that it will return a Song that meets quotas.
    # 
    # @param female True if the song should include a female artist, False to select any song.
    #
    def getRandomSong(self, female): 
        cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if female == True:
            cur.execute("SELECT * FROM cd WHERE female = '2' ORDER BY RANDOM() LIMIT 1")
        else:
            cur.execute("SELECT * FROM cd ORDER BY RANDOM() LIMIT 1")

        cd = cur.fetchone()
        cur.execute("SELECT * from cdtrack WHERE cdid = %s ORDER BY RANDOM() LIMIT 1;", (cd['id'],))
        track = cur.fetchone()
        return Song(cd, track)

