
from Song import Song
import psycopg2
import psycopg2.extras

class MusicLibrary:

    def __init__(self, databaseConnection):
        self.db = databaseConnection

    def setAustralianNames(self, names):
        self.ausNames = names


    def getRandomDemo(self):
        cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM cd WHERE demo = '2' ORDER BY RANDOM() LIMIT 1")
        cd = cur.fetchone()
        cur.execute("SELECT * from cdtrack WHERE cdid = %s ORDER BY RANDOM() LIMIT 1;", (cd['id'],))
        track = cur.fetchone()
        return Song(cd, track)

    def getRandomLocal(self):
        cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM cd WHERE local = '2' ORDER BY RANDOM() LIMIT 1")
        cd = cur.fetchone()
        cur.execute("SELECT * from cdtrack WHERE cdid = %s ORDER BY RANDOM() LIMIT 1;", (cd['id'],))
        track = cur.fetchone()
        return Song(cd, track)

    def getRandomAustralian(self): 
        cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM cd WHERE cpa = ANY(%s) ORDER BY RANDOM() LIMIT 1", (self.ausNames,))
        cd = cur.fetchone()
        cur.execute("SELECT * from cdtrack WHERE cdid = %s ORDER BY RANDOM() LIMIT 1;", (cd['id'],))
        track = cur.fetchone()
        return Song(cd, track)

    def getRandomSong(self, female): 
        cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if female == True:
            cur.execute("SELECT * FROM cd WHERE female = '2' ORDER BY RANDOM() LIMIT 1")
        else:
            cur.execute("SELECT * FROM cd ORDER BY RANDOM() LIMIT 1")

        cd = cur.fetchone()
        cur.execute("SELECT * from cdtrack WHERE cdid = %s ORDER BY RANDOM() LIMIT 1;", (cd['id'],))
        track = cur.fetchone()
        return Song(cd, track)

