

class Song:
    def __init__(self, cdInfo, trackInfo):
        self.cdInfo = cdInfo
        self.trackInfo = trackInfo

    # title stuff
    def getTrackTitle(self):
        return self.trackInfo['tracktitle']

    def getArtistName(self):
        if not self.trackInfo['trackartist']:
            return self.cdInfo['artist']
        else:
            return self.trackInfo['trackartist']

    def getDetails(self):
        return self.getArtistName() + ' - ' + self.getTrackTitle()

    def setLocalPath(self, path):
        self.path = path

    def getLocalPath(self):
        return self.path

    # IDs
    def getReleaseID(self):
        return self.cdInfo['id']

    def getTrackID(self):
        return self.trackInfo['trackid']

    def getTrackNumber(self):
        return self.trackInfo['tracknum']

    # Quota Stuff
    def isLocal(self):
        return self.cdInfo['local'] == 2
    
    def isAustralian(self):
        return self.cdInfo['cpa'] in Song.ausNames

    def isDemo(self):
        return self.cdInfo['demo'] == 2

    def hasFemale(self):
        return self.cdInfo['female'] == 2
