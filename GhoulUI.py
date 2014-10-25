import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import threading
import PlayItem
import time


class GhoulUI:

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def __init__(self, controller):        
        self.gladeFile = "MainGUI.glade"
        self.glade = gtk.Builder()
        self.glade.add_from_file(self.gladeFile)

        dic = { "onPause" : self.onPause,
                "onPlay" :  self.onPlay,
                "onWindowClose" : self.onClose
                }

        self.controller = controller
        self.controller.addListener(self)
        self.glade.connect_signals(dic)

        self.glade.get_object("MainWindow").show_all()

        self.nowPlaying = None

    def main(self):
        gLoop = threading.Thread(target=gtk.main);
        gLoop.start()

    def progressBarUpdate(self):
        while True:
            try:
                if self.nowPlaying != None:
                    duration = self.nowPlaying.getDuration()
                    currentTime = self.controller.getElapsedTime()
                    self.glade.get_object("SongProgress").set_fraction( float(currentTime) / (duration * 1000))
                    elapsedMinutes = (currentTime / 1000) / 60
                    elapsedSeconds = (currentTime / 1000) % 60
                    totalMinutes = duration / 60
                    totalSeconds = duration % 60
                    self.glade.get_object("SongProgress").set_text("%01d:%02d / %01d:%02d" %(elapsedMinutes, elapsedSeconds, totalMinutes, totalSeconds))
                time.sleep(0.2)
            except:
                pass


    def onPlay(self, widget):
        self.glade.get_object("PlayButton").set_sensitive(False)
        self.glade.get_object("PauseButton").set_sensitive(True)
        self.controller.play()
        gLoop = threading.Thread(target=self.progressBarUpdate);
        gLoop.daemon = True
        gLoop.start()

    def onPause(self, widget):
        self.controller.pause()
        self.glade.get_object("PlayButton").set_sensitive(True)
        self.glade.get_object("PauseButton").set_sensitive(False)


    def onClose(self, widget):
        gtk.main_quit()

    def itemQueued(self, item):
        items = self.controller.getQueuedItems()
        self.glade.get_object("queue").clear()
        for i in items:
            data = list()
            if isinstance(i, PlayItem.Message):
                data.append(i.getCategory())
                data.append(i.getTitle())
                data.append("")
                data.append("")
                data.append("")
                data.append("")
            else:
                data.append(i.getArtistName())
                data.append(i.getTrackTitle())
                if i.isDemo():
                    data.append("X")
                else:
                    data.append("")
                if i.isLocal():
                    data.append("X")
                else:
                    data.append("")
                if i.isAustralian():
                    data.append("X")
                else:
                    data.append("")
                if i.hasFemale():
                    data.append("X")
                else:
                    data.append("")

            self.glade.get_object("queue").append(data)


    def itemPlaying(self, item):
        if self.nowPlaying != None:
            data = list()
            if isinstance(self.nowPlaying, PlayItem.Message):
                data.append(self.nowPlaying.getCategory())
                data.append(self.nowPlaying.getTitle())
                data.append("")
                data.append("")
                data.append("")
                data.append("")
            else:
                data.append(self.nowPlaying.getArtistName())
                data.append(self.nowPlaying.getTrackTitle())
                if self.nowPlaying.isDemo():
                    data.append("X")
                else:
                    data.append("")
                if self.nowPlaying.isLocal():
                    data.append("X")
                else:
                    data.append("")
                if self.nowPlaying.isAustralian():
                    data.append("X")
                else:
                    data.append("")
                if self.nowPlaying.hasFemale():
                    data.append("X")
                else:
                    data.append("")

            self.glade.get_object("history").insert(0, data)

        self.nowPlaying = item
        self.glade.get_object("NowPlayingLabel").set_label(item.getDetails())


    def onStartPlaying(self, item):
        pass

    def onEndTrack(self, item):
        pass

