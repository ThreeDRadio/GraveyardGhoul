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


import requests
from Song import Song


##
# The FileManager class is responsible for actually getting playable files
# from entries in the catalogue.
#
# This particular class gets songs from Three D Radio's intranet, and should
# only be used for testing.
#
class FileManager:
    def __init__(self, userID, passwordHash, httpUser, httpPass):
        self.mode = "external"
        self.auth = (httpUser, httpPass)
        self.cookies = dict(threed_id=format(userID, "d"), threed_password=passwordHash)

    ##
    # Returns true if there is actually a file for the song.
    #
    # Not all the entries in the database have actually been ripped, such as vinyl.
    # We want to make sure we only try to play Songs that have actually been ripped to MP3.
    #
    # @param song The song to check
    # @return True if the song has been ripped, False otherwise.
    #
    def fileExists(self, song):
        songURL = self.constructURL(song)
        r = requests.head(url=songURL, auth = self.auth, cookies = self.cookies)
        return r.headers['Content-Type'] == 'audio/mpeg'


    ##
    # Prepares a Song for playback (for example, cache a remote file)
    #
    # @param song The Song to prepare.
    #
    def prepare(self, song):
        if isinstance(song, Song):
            songURL = self.constructURL(song)
            r = requests.get(url=songURL, auth = self.auth, cookies = self.cookies)
            f = open('/tmp/' + `song.getTrackID()` + '.mp3', 'w')
            song.setLocalPath('/tmp/' + `song.getTrackID()` + '.mp3')
            f.write(r.content)


    ##
    # Gets the system path for a song.
    #
    # @param song The Song we need the path for
    def getPath(self, song):
        return "/tmp/" + `song.getTrackID()` + ".mp3"

    ##
    # Constructs a URL for obtaining a Song from Three D's intranet
    # 
    # @param song The Song to process
    # @return the URL for the intranet where the mp3 can be retrieved.
    def constructURL(self, song):
        paddedRelease= format (song.getReleaseID(), "07d")
        paddedTrack  = format (song.getTrackNumber(), "02d")
        url = "http://intranet.threedradio.com/database/play/" + paddedRelease + "-" + paddedTrack + "-lo.mp3"
        return url
