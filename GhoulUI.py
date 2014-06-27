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
        self.glade.connect_signals(self)
        self.glade.get_object("MainWindow").show_all()

    def main(self):
        gtk.main();


