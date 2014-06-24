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

    ##
    # Adds some songs to the queue.
    # Can be called before starting the thread, because some FileManager modes
    # take a while to buffer.
    #
    # @param count The number of itmes to add.
    def seedQueue(self, count):
        for i  in range(count):
            item = self.getNextItem()
            print "Loading: " + item.getDetails()
            self.fileManager.prepare(item)
            self.playQueue.put(item)


    ##
    # Called by thread.start, loops forever adding items to the play queue
    #
    def run(self):
        while True:
            item = self.getNextItem()
            print "Loading: " + item.getDetails()
            self.fileManager.prepare(item)
            self.playQueue.put(item)
            self.printStats()

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
    # Gets the next item that should be played.
    #
    # This method is a little bit clever, it randomly selects items to play
    # in such a way that the quotas are met.
    # 
    # @return The next item to queue
    def getNextItem(self):
        i = 0
        while True: 
            i+=1
            if self.playCount < 5:
                nextSong = self.music.getRandomSong(False)

            # After 5 totally random tracks, we have enough to start working towards quotas...
            else:
                if self.demoCount / float(self.playCount) < self.demoQuota:
                    nextSong = self.music.getRandomDemo()

                elif self.localCount / float(self.playCount) < self.localQuota:
                    nextSong = self.music.getRandomLocal()

                elif self.ausCount / float(self.playCount) < self.ausQuota:
                    nextSong = self.music.getRandomAustralian()

                elif self.femaleCount / float(self.playCount) < self.femaleQuota:
                    nextSong = self.music.getRandomSong(True)

                else:
                    nextSong = self.music.getRandomSong(False)

            self.totalRequests += 1
            if self.fileManager.fileExists(nextSong):
                break;
        self.addToPlayCount(nextSong)
        return nextSong


    ##
    # Prints some quota statistics
    def printStats(self):
        print "Songs Played:    " + `self.playCount`
        print "Songs Requested: " + `self.totalRequests`
        print "Demos:           " + `self.demoCount`
        print "Local:           " + `self.localCount`
        print "Aus:             " + `self.ausCount`
        print "Female:          " + `self.femaleCount`

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

