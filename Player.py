#                                                             
#          # ###        /                             ###     
#        /  /###  /   #/                               ###    
#       /  /  ###/    ##                                ##    
#      /  ##   ##     ##                                ##    
#     /  ###          ##                                ##    
#    ##   ##          ##  /##      /###   ##   ####     ##    
#    ##   ##   ###    ## / ###    / ###  / ##    ###  / ##    
#    ##   ##  /###  / ##/   ###  /   ###/  ##     ###/  ##    
#    ##   ## /  ###/  ##     ## ##    ##   ##      ##   ##    
#    ##   ##/    ##   ##     ## ##    ##   ##      ##   ##    
#     ##  ##     #    ##     ## ##    ##   ##      ##   ##    
#      ## #      /    ##     ## ##    ##   ##      ##   ##    
#       ###     /     ##     ## ##    ##   ##      /#   ##    
#        ######/      ##     ##  ######     ######/ ##  ### / 
#          ###         ##    ##   ####       #####   ##  ##/  
#                            /                                
#                           /                                 
#                          /                                  
#                         /                                   
#
#  Haunting Three D Radio's Graveyard Slots
#  Copyright 2014 Michael Marner <michael@20papercups.net>
#  Release under MIT Licence




import pygst
pygst.require("0.10")
import gst
import os



##
# This class plays audio as requested.
#
class Player:
    
    ##
    # Constructor, builds a gstreamer player ready to play music
    #
    def __init__(self):
        self.pipeline = gst.Pipeline("RadioPipe")
        self.player = gst.element_factory_make("playbin2", "player")
        self.fakesink = gst.element_factory_make("fakesink", "fakesink")
        self.output = gst.element_factory_make("autoaudiosink", "audiosink")
        #self.output.set_property("device", "preview")
        self.player.set_property("video-sink", self.fakesink)
        #self.player.set_property("audio-sink", self.output)
        self.pipeline.add(self.player)
        self.player.connect("about-to-finish", self.finished)


    ##
    # Adds a listener to this object, which will be notified when playing finishes
    #
    def addListener(self, listener):
        self.listener = listener

    ##
    # Start playing some content.
    #
    # @param path The full path to the content to play (file, url, etc.)
    #
    def playContent(self, path):
        self.pipeline.set_state(gst.STATE_NULL)
        self.player.set_property("uri", "file://" + path)
        #self.player.set_property('uri', 'file://' + os.path.abspath('test.mp3'))
        self.pipeline.set_state(gst.STATE_PLAYING)

    ##
    # Private callback function, you shouldn't touch this.
    def finished(self, data):
        self.listener.finished()

