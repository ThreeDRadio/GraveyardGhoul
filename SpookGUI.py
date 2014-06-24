import pygtk
pygtk.require('2.0')
import gtk


class GUI(gtk.Window):

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def __init__(self):        
        gtk.Window.__init__(self)
        self.gladefile = "window.glade"



    def main(self):
        gtk.main();


