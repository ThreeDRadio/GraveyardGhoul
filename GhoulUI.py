import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade


class GhoulUI:

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def __init__(self):        
        self.gladeFile = "MainGUI.glade"
        self.glade = gtk.Builder()
        self.glade.add_from_file(self.gladeFile)

        dic = { "onPause" : self.onPause,
                "onPlay" :  self.onPlay,
                "onStop" :  self.onStop,
                "onWindowClose" : self.onClose
                }

        self.glade.connect_signals(dic)

        self.glade.get_object("MainWindow").show_all()

    def main(self):
        gtk.main();

    def onPlay(self, widget):
        print "Play Pressed"

    def onPause(self, widget):
        print "Pause Pressed"

    def onStop(self, widget):
        print "Stop Pressed"

    def onClose(self, widget):
        gtk.main_quit()
