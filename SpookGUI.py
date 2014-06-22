import pygtk
pygtk.require('2.0')
import gtk


class SpookGUI(gtk.Window):

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def __init__(self):        
        gtk.Window.__init__(self)
        self.set_title("Spook - Haunting the Three D Graveyards");
        self.show()


    def main(self):
        gtk.main();


