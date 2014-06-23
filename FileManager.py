

from Song import Song


class FileManager:
    def __init__(self):
        self.mode = "test"

    def getFile(self, song):
        return file("/Users/michael/test.mp3")
