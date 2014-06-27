#!./env/bin/python

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

   
import glib, gobject
import yaml
import psycopg2
import threading

from FileManager import FileManager

from MusicLibrary import MusicLibrary
from MessageLibrary import MessageLibrary
import Player
import PlayItem

import GhoulUI 
from Scheduler import Scheduler
from Queue import Queue


class Ghoul:
    def __init__(self):
        configStream = file('config.yaml', 'r')
        config = yaml.load(configStream)

        self.libraryDB = psycopg2.connect(host = config['music_database']['host'],
                                     user = config['music_database']['user'],
                                     password = config['music_database']['password'],
                                     database = config['music_database']['database'])
        
        self.messageDB = psycopg2.connect(host = config['msg_database']['host'],
                                     user = config['msg_database']['user'],
                                     password = config['msg_database']['password'],
                                     database = config['msg_database']['database'])
        
        
        self.fm = FileManager(config['file_manager']['user_id'], 
                         config['file_manager']['password'],
                         config['file_manager']['httpUser'],
                         config['file_manager']['httpPass'])

        self.library = MusicLibrary(self.libraryDB)
        self.library.setAustralianNames(config['music']['aus_names'])
        self.library.setMaxSongLength(config['music']['max_song_length'])
        PlayItem.Song.ausNames = config['music']['aus_names']
        
        self.messages = MessageLibrary(self.messageDB)
        self.messages.setStingCategories(config['messages']['sting_categories'])
        PlayItem.Message.basePath = config['file_manager']['message_base_path']
        
        self.playQueue = Queue(5)
       
        self.scheduler = Scheduler(self.library, self.messages, self.fm, self.playQueue)
        self.scheduler.setDemoQuota(config['scheduler']['quotas']['demo'])
        self.scheduler.setLocalQuota(config['scheduler']['quotas']['local'])
        self.scheduler.setAusQuota(config['scheduler']['quotas']['aus'])
        self.scheduler.setFemaleQuota(config['scheduler']['quotas']['female'])
        self.scheduler.setConsecutiveSongs(config['scheduler']['consecutive_songs']['min'],
                                      config['scheduler']['consecutive_songs']['max'])

        self.player = Player.Player()
        self.playThread = Player.PlayThread(self.player, self.playQueue)

        self.paused = False

    def play(self):
        if self.paused:
            self.paused = False
            self.player.togglePause()
        else:
            self.scheduler.start()
            self.playThread.start()

    def pause(self):
        self.paused = True
        self.player.togglePause()





print "Ghoul - The Three D Radio Graveyard Manager"
print "Copyright 2014 Michael Marner <michael@20papercups.net>"
gobject.threads_init()

ghoul = Ghoul()
gui = GhoulUI.GhoulUI(ghoul)
gui.main()

print "GUI Loaded"

