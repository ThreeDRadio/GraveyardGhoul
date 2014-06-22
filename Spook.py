#!./env/bin/python
import yaml
from SpookGUI import SpookGUI 
from MusicLibrary import MusicLibrary

print "Spook - The Three D Radio Graveyard Manager"
print "Copyright 2014 Michael Marner <michael@20papercups.net>"

print "Loading config file... "
configStream = file('config.yaml', 'r')
config = yaml.load(configStream)
yaml.dump(config)



#gui = SpookGUI()
#gui.main()


print "GUI Loaded"

