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

import threading
from PlayItem import Song
from PlayItem import Message
import random

##
# Class responsible for scheduling items to play.
# Can be called manually, or started as a thread.
class Scheduler(threading.Thread):

    ##
    # Constructs a new Schedular object.
    #
    # @param musicLibrary The MusicLibrary object to query
    # @param messageLibrary The MessageLibrary object to query
    # @param fileManager The FileManager object used to resolve Songs to files
    # @param playQueue The Queue to add scheduled items to
    def __init__(self, musicLibrary, messageLibrary, fileManager, playQueue):
        threading.Thread.__init__(self)
        self.daemon = True
        self.music = musicLibrary
        self.messages = messageLibrary
        self.fileManager = fileManager
        self.playQueue = playQueue

        self.demoQuota = 0
        self.localQuota = 0
        self.ausQuota = 0
        self.femaleQuota = 0

        self.minConsecutive = 0
        self.maxConsecutive = 0

        self.resetPlayCount()

        self.listeners = list()

    ##
    # Called by thread.start, loops forever adding items to the play queue
    #
    def run(self):
        while True:
            item = self.getNextItem()
            print("Loading: " + item.getDetails())
            self.fileManager.prepare(item)
            self.playQueue.put(item)
            for l in self.listeners:
                l.itemQueued(item)

    ##
    # Resets the play count and quota counts.
    #
    def resetPlayCount(self):
        self.playCount = 0
        self.demoCount = 0
        self.localCount = 0
        self.ausCount = 0
        self.femaleCount = 0
        self.consecutiveSongs = 0
        self.totalRequests = 0

    ##
    # Get's the next song
    #
    def getNextSong(self):
        if self.demoCount / float(self.playCount) < self.demoQuota:
            nextItem = self.music.getRandomDemo()

        elif self.localCount / float(self.playCount) < self.localQuota:
            nextItem = self.music.getRandomLocal()

        elif self.ausCount / float(self.playCount) < self.ausQuota:
            nextItem = self.music.getRandomAustralian()

        elif self.femaleCount / float(self.playCount) < self.femaleQuota:
            nextItem = self.music.getRandomSong(True)

        else:
            nextItem = self.music.getRandomSong(False)

    ##
    # Gets the next item that should be played.
    #
    # This method is a little bit clever, it randomly selects items to play
    # in such a way that the quotas are met.
    # 
    # @return The next item to queue
    def getNextItem(self):
        while True: 
            if self.playCount < 5:
                nextItem = self.music.getRandomSong(False)

            # After 5 totally random tracks, we have enough to start working towards quotas...
            else:
                # absolutely must play a sting...
                if self.consecutiveSongs >= self.maxConsecutive:
                    nextItem = self.messages.getRandomSting()
                elif self.consecutiveSongs >= self.minConsecutive:
                    coin = random.randint(0, self.maxConsecutive - self.consecutiveSongs)
                    if coin == 0:
                        nextItem = self.messages.getRandomSting()
                    else:
                        nextItem = self.getNextSong()
                else:
                    nextItem = self.getNextSong()

            if isinstance(nextItem, Song):
                self.totalRequests += 1
                if self.fileManager.fileExists(nextItem):
                    self.addToPlayCount(nextItem)
                    break;
            else:
                self.consecutiveSongs = 0
                break;
        return nextItem


    ##
    # Prints some quota statistics
    def printStats(self):
        print("Songs Played:    " + str(self.playCount))
        print("Songs Requested: " + str(self.totalRequests))
        print("Demos:           " + str(self.demoCount))
        print("Local:           " + str(self.localCount))
        print("Aus:             " + str(self.ausCount))
        print("Female:          " + str(self.femaleCount))

    ##
    # Adds the song to the play count stats
    # @param nextSong the song to add to the stats.
    #
    def addToPlayCount(self, nextSong):
        self.playCount += 1
        self.consecutiveSongs+=1
        if nextSong.isDemo():
            self.demoCount+=1
        if nextSong.isLocal():
            self.localCount+=1
        if nextSong.isAustralian():
            self.ausCount+=1
        if nextSong.hasFemale():
            self.femaleCount+=1

    
    def setConsecutiveSongs(self, minSongs, maxSongs):
        self.minConsecutive = minSongs
        self.maxConsecutive = maxSongs 


    ##
    # Sets the demo quota to aim for, as a number between 0-1
    def setDemoQuota(self, quota):
        self.demoQuota = quota

    ##
    # Sets the local quota to aim for, as a number between 0-1
    def setLocalQuota(self, quota):
        self.localQuota = quota

    ##
    # Sets the Australian quota to aim for, as a number between 0-1
    def setAusQuota(self, quota):
        self.ausQuota = quota

    ##
    # Sets the Female quota to aim for, as a number between 0-1
    def setFemaleQuota(self, quota):
        self.femaleQuota = quota

    def addListener(self, listener):
        self.listeners.append(listener)

