import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade


class GhoulUI():

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def __init__(self):        
        pass

    def main(self):
        gtk.main();


