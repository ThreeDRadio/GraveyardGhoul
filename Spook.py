#!./env/bin/python
import yaml
import psycopg2
from FileManager import FileManager
from MusicLibrary import MusicLibrary
from SpookGUI import SpookGUI 
from Scheduler import Scheduler
from Song import Song

print "Spook - The Three D Radio Graveyard Manager"
print "Copyright 2014 Michael Marner <michael@20papercups.net>"

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


library = MusicLibrary(libraryDB)
library.setAustralianNames(config['music']['aus_names'])
Song.ausNames = config['music']['aus_names']

scheduler = Scheduler(library, 0)
scheduler.setDemoQuota(config['scheduler']['quotas']['demo'])
scheduler.setLocalQuota(config['scheduler']['quotas']['local'])
scheduler.setAusQuota(config['scheduler']['quotas']['aus'])
scheduler.setFemaleQuota(config['scheduler']['quotas']['female'])

for i in range(40):
    item = scheduler.getNextItem()
    item.printDetails()
#    if i % 5 == 0:
#        scheduler.printStats()

scheduler.printStats()

#gui = SpookGUI()
#gui.main()


print "GUI Loaded"

