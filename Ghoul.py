#!./env/bin/python
import glib, gobject
import yaml
import psycopg2
from FileManager import FileManager
from MusicLibrary import MusicLibrary
from Player import Player 
from PlayThread import PlayThread
from GhoulUI import GhoulUI 
from Scheduler import Scheduler
from Song import Song
from Queue import Queue
import threading

print "Ghoul - The Three D Radio Graveyard Manager"
print "Copyright 2014 Michael Marner <michael@20papercups.net>"

gobject.threads_init()

print "Loading config file... "
configStream = file('config.yaml', 'r')
config = yaml.load(configStream)
yaml.dump(config)

print "Connecting to database"
libraryDB = psycopg2.connect(host = config['music_database']['host'],
                             user = config['music_database']['user'],
                             password = config['music_database']['password'],
                             database = config['music_database']['database'])

messageDB = psycopg2.connect(host = config['msg_database']['host'],
                             user = config['msg_database']['user'],
                             password = config['msg_database']['password'],
                             database = config['msg_database']['database'])

fm = FileManager(config['file_manager']['user_id'], 
                 config['file_manager']['password'],
                 config['file_manager']['httpUser'],
                 config['file_manager']['httpPass'])

library = MusicLibrary(libraryDB)
library.setAustralianNames(config['music']['aus_names'])
Song.ausNames = config['music']['aus_names']

playQueue = Queue(5)

scheduler = Scheduler(library, 0, fm, playQueue)
scheduler.setDemoQuota(config['scheduler']['quotas']['demo'])
scheduler.setLocalQuota(config['scheduler']['quotas']['local'])
scheduler.setAusQuota(config['scheduler']['quotas']['aus'])
scheduler.setFemaleQuota(config['scheduler']['quotas']['female'])

print "Starting the scheduler thread"
scheduler.start()
player = Player()
playThread = PlayThread(player, playQueue)
playThread.start()
    

scheduler.printStats()

gui = GhoulUI()
gui.main()


print "GUI Loaded"
