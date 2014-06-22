#!./env/bin/python
import pygtk
pygtk.require('2.0')
import gtk
from SpookGUI import SpookGUI 

print "Spook - The Three D Radio Graveyard Manager"
print "Copyright 2014 Michael Marner <michael@20papercups.net>"

gui = SpookGUI()
gui.main()

print "GUI Loaded"

