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
#  Copyright 2016 Michael Marner <michael@20papercups.net>
#  Release under MIT Licence

import requests
import time
from datetime import date
from datetime import datetime

class PlaylistLogger:

    def __init__(self, auth, baseURL, showID):
        self.auth = auth
        self.baseURL = baseURL
        self.showID = showID

    def startNewPlaylist(self):
        headers = {
                "Authorization" : "Token " + self.auth,
                }

        data = {
                'show': self.showID,
                'date': date.today().isoformat(),
                'notes': 'Ghoul started at ' + datetime.now().strftime('%H:%M'),
                'host': 'Graveyard Ghoul'
        }

        r = requests.post(self.baseURL + '/playlists/', headers=headers, data=data)
        response = r.json()
        
        self.playlistID = response['id'];
        return response['id'];


    def submitSong(self, song):
        headers = {
                "Authorization" : "Token " + self.auth,
                }

        data = {
                'playlist': self.playlistID,
                'playlist_id': self.playlistID,
                'artist': song.getArtistName(),
                'title': song.getTrackTitle(),
                'album': song.getReleaseName(),
                'duration': song.duration,
                'local': song.isLocal(),
                'australian': song.isAustralian(),
                'female':  song.hasFemale(),
                'newRelease': 'false' # we don't want Ghoul in Top 20+1
        }
        r = requests.post(self.baseURL + '/playlistentries/', headers=headers, data=data)

