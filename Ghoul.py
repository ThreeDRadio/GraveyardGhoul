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

   
import yaml
import psycopg2
import threading
import gtk
import sys

from FileManager import LocalFileManager
from FileManager import ExternalFileManager

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
        
        try:
            self.messageDB = psycopg2.connect(host = config['msg_database']['host'],
                                     user = config['msg_database']['user'],
                                     password = config['msg_database']['password'],
                                     database = config['msg_database']['database'])
        
            self.messages = MessageLibrary(self.messageDB)
            self.messages.setStingCategories(config['messages']['sting_categories'])
            PlayItem.Message.basePath = config['file_manager']['message_base_path']
        except TypeError:
            pass
        finally:
            self.messages = None
        
        if config['file_manager']['mode'] == "external":
            self.fm = ExternalFileManager(config['file_manager']['user_id'], 
                             config['file_manager']['password'],
                             config['file_manager']['httpUser'],
                             config['file_manager']['httpPass'])

        elif config['file_manager']['mode'] == 'local':
            self.fm = LocalFileManager(config['file_manager']['music_base_path'])


        self.library = MusicLibrary(self.libraryDB)
        self.library.setAustralianNames(config['music']['aus_names'])
        self.library.setMaxSongLength(config['music']['max_song_length'])
        PlayItem.Song.ausNames = config['music']['aus_names']
        
        
        self.playQueue = Queue(5)
       
        self.scheduler = Scheduler(self.library, self.messages, self.fm, self.playQueue)
        self.scheduler.setDemoQuota(config['scheduler']['quotas']['demo'])
        self.scheduler.setLocalQuota(config['scheduler']['quotas']['local'])
        self.scheduler.setAusQuota(config['scheduler']['quotas']['aus'])
        self.scheduler.setFemaleQuota(config['scheduler']['quotas']['female'])
        self.scheduler.setConsecutiveSongs(config['scheduler']['consecutive_songs']['min'],
                                      config['scheduler']['consecutive_songs']['max'])

        self.scheduler.addListener(self)

        self.player = Player.Player()
        self.playThread = Player.PlayThread(self.player, self.playQueue)
        self.playThread.addListener(self)

        self.paused = False

        self.listeners = list()

    def addListener(self, listener):
        self.listeners.append(listener)


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

    def getElapsedTime(self):
        return self.player.getElapsedTime()

    def getQueuedItems(self):
        items = list()
        for elem in list(self.playQueue.queue):
            items.append(elem)
        return items


    def itemPlaying(self, item):
        for l in self.listeners:
            l.itemPlaying(item)

    def itemQueued(self, item):
        for l in self.listeners:
            l.itemQueued(item)

print "Ghoul - The Three D Radio Graveyard Manager"
print "Copyright 2015 Michael Marner <michael@20papercups.net>"
gtk.gdk.threads_init()

ghoul = Ghoul()
gui = GhoulUI.GhoulUI(ghoul)
gui.main()

print "GUI Loaded"

if "--autoplay" in sys.argv:
    print "Autoplay"
    gui.onPlay(None)


