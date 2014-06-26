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

from PlayItem import Message
import psycopg2
import psycopg2.extras


##
# Abstraction around the music library database
class MessageLibrary:

    ##
    # Constructor.
    # 
    # @param databaseConnection the Psycopg2 object connected to the message database
    def __init__(self, databaseConnection):
        self.db = databaseConnection

    ##
    # Sets the list of categories for stings/stationIDs.
    # @param names the list of category names for stings
    #
    def setStingCategories(self, names):
        self.stings = names


    ##
    # Returns a random sting from the library.
    #
    def getRandomSting(self):
        cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM messagelist WHERE type = ANY(%s) ORDER BY RANDOM() LIMIT 1", (self.stings,))
        details = cur.fetchone()
        return Message(details['type'], details['code'], details['filename'])

