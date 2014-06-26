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

import urllib

class PlayItem:
    ##
    # Store the local path for the file for this song. Used by FileManager.
    # @param path The path to the file for this song.
    def setLocalPath(self, path):
        self.path = path

    ##
    # Returns the local path for this file
    def getLocalPath(self):
        return self.path

    ##
    # Returns a friendly string for printing to log files, etc.
    def getDetails(self):
        pass

    ##
    # Returns this song's info as a CSV line
    def getCSVLine(self):
        pass


class Message(PlayItem):
    def __init__(self, category, code, filename):
        self.category = category
        self.filename = filename
        catPath = category.lower()[:12]
        #self.setLocalPath(urllib.quote(Message.basePath + catPath + '/' + filename ))
        self.setLocalPath(Message.basePath + catPath + '/' + filename)
        self.code = code

    def getDetails(self):
        return self.category + " - " + self.code


##
# Represents a single song from the music catalogue
#
class Song(PlayItem):
    ##
    # Constructor, takes the data from the database to encapsulate
    # @param cdInfo the dictionary of data fro the row in the CD table
    # @param trackInfo the dictionary of data fro the row in the cdtrack table
    def __init__(self, cdInfo, trackInfo):
        self.cdInfo = cdInfo
        self.trackInfo = trackInfo

    ##
    # Returns the title of the track.
    def getTrackTitle(self):
        return self.trackInfo['tracktitle']

    ##
    # Returns the name of the artist.
    def getArtistName(self):
        if not self.trackInfo['trackartist']:
            return self.cdInfo['artist']
        else:
            return self.trackInfo['trackartist']

    ##
    # Returns a friendly string for printing to log files, etc.
    def getDetails(self):
        return self.getArtistName() + ' - ' + self.getTrackTitle()

    ##
    # Returns this song's info as a CSV line
    def getCSVLine(self):
        return '"' + self.getArtistName() + '",' + \
               '"' + self.getTrackTitle() + '",' + \
               '"' + `self.isDemo()` + '",' + \
               '"' + `self.isLocal()` + '",' + \
               '"' + `self.isAustralian()` + '",' + \
               '"' + `self.hasFemale()`  +'"'


    ##
    # Returns the release ID
    def getReleaseID(self):
        return self.cdInfo['id']

    ##
    # Returns the track ID used by the database.
    def getTrackID(self):
        return self.trackInfo['trackid']

    ##
    # Returns the track number from this song's release.
    def getTrackNumber(self):
        if self.trackInfo == None:
            return 0
        return self.trackInfo['tracknum']

    def isLocal(self):
        return self.cdInfo['local'] == 2
    
    def isAustralian(self):
        return self.cdInfo['cpa'] in Song.ausNames

    def isDemo(self):
        return self.cdInfo['demo'] == 2

    def hasFemale(self):
        return self.cdInfo['female'] == 2
