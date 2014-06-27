import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import threading


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
        self.glade.connect_signals(dic)

        self.glade.get_object("MainWindow").show_all()

    def main(self):
        gLoop = threading.Thread(target=gtk.main);
        gLoop.start()

    def onPlay(self, widget):
        self.glade.get_object("PlayButton").set_sensitive(False)
        self.glade.get_object("PauseButton").set_sensitive(True)
        self.controller.play()

    def onPause(self, widget):
        self.controller.pause()
        self.glade.get_object("PlayButton").set_sensitive(True)
        self.glade.get_object("PauseButton").set_sensitive(False)


    def onClose(self, widget):
        gtk.main_quit()
