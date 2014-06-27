#!./env/bin/python
import glib, gobject
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
from GhoulUI import GhoulUI 
import threading
gobject.threads_init()
gLoop = threading.Thread(target=gtk.main)
gLoop.start()
gui = GhoulUI()
