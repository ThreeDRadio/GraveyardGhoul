


class Scheduler:

    def __init__(self, musicLibrary, messageLibrary):
        self.music = musicLibrary
        self.messages = messageLibrary

        self.demoQuota = 0
        self.localQuota = 0
        self.ausQuota = 0
        self.femaleQuota = 0

        self.minConsecutive = 0
        self.maxConsecutive = 0

        self.resetPlayCount()


    def resetPlayCount(self):
        self.playCount = 0
        self.demoCount = 0
        self.localCount = 0
        self.ausCount = 0
        self.femaleCount = 0
        self.consecutiveSongs = 0

    def getNextItem(self):
        if self.playCount < 5:
            nextSong = self.music.getRandomSong(False)
            self.addToPlayCount(nextSong)
            return nextSong

        # After 5 totally random tracks, we have enough to start working towards quotas...
        else:
            if self.demoCount / float(self.playCount) < self.demoQuota:
                nextSong = self.music.getRandomDemo()
                self.addToPlayCount(nextSong)
                return nextSong

            elif self.localCount / float(self.playCount) < self.localQuota:
                nextSong = self.music.getRandomLocal()
                self.addToPlayCount(nextSong)
                return nextSong

            elif self.ausCount / float(self.playCount) < self.ausQuota:
                nextSong = self.music.getRandomAustralian()
                self.addToPlayCount(nextSong)
                return nextSong

            elif self.femaleCount / float(self.playCount) < self.femaleQuota:
                nextSong = self.music.getRandomSong(True)
                self.addToPlayCount(nextSong)
                return nextSong

            else:
                nextSong = self.music.getRandomSong(False)
                self.addToPlayCount(nextSong)
                return nextSong


    def printStats(self):
        print "Songs:  " + `self.playCount`
        print "Demos:  " + `self.demoCount`
        print "Local:  " + `self.localCount`
        print "Aus:    " + `self.ausCount`
        print "Female: " + `self.femaleCount`

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



    def setDemoQuota(self, quota):
        self.demoQuota = quota

    def setLocalQuota(self, quota):
        self.localQuota = quota

    def setAusQuota(self, quota):
        self.ausQuota = quota

    def setFemaleQuota(self, quota):
        self.femaleQuota = quota


