

import requests
from Song import Song


class FileManager:
    def __init__(self, userID, passwordHash, httpUser, httpPass):
        self.mode = "external"
        self.auth = (httpUser, httpPass)
        self.cookies = dict(threed_id=format(userID, "d"), threed_password=passwordHash)

    def fileExists(self, song):
        songURL = self.constructURL(song)
        r = requests.head(url=songURL, auth = self.auth, cookies = self.cookies)
        if r.headers['Content-Type'] == 'audio/mpeg':
            print "matching" + song.getDetails()
            return True
        else:
            print "Not matching!" + r.headers['content-type']
            return False


    def getFile(self, song):

        return file("/Users/michael/test.mp3")

    def constructURL(self, song):
        paddedRelease= format (song.getReleaseID(), "07d")
        paddedTrack  = format (song.getTrackNumber(), "02d")
        url = "http://intranet.threedradio.com/database/play/" + paddedRelease + "-" + paddedTrack + "-lo.mp3"
        return url
