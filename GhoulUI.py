import pygtk
pygtk.require('2.0')
import gtk


class GhoulUI():

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def __init__(self):        
        self.window = gtk.Window()
        self.window.set_title("Graveyard Ghoul")
        self.window.show()

    def main(self):
        gtk.main();


