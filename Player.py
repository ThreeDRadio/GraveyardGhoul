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




try:
    import pygst
    pygst.require("0.10")
    import gst
except:
    from gi.repository import Gst as gst

import os
import urllib
import threading 


##
# This class plays audio as requested.
#
class Player:
    
    ##
    # Constructor, builds a gstreamer player ready to play music
    #
    def __init__(self):
        try:
          self.player = gst.element_factory_make("playbin2", "player")
        except:
          self.player = gst.ElementFactory.make('playbin2', "player")

        #self.player.connect("about-to-finish", self.finished)
        self.bus = self.player.get_bus()
        self.bus.connect('message', self.onMessage)
        self.bus.add_signal_watch()
        self.paused = False


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
        self.player.set_state(gst.STATE_NULL)
        self.player.set_property("uri", "file://" + urllib.pathname2url(path))
        self.player.set_state(gst.STATE_PLAYING)
        self.paused = False

    def stop(self):
        self.player.set_state(gst.STATE_PAUSED)
        self.paused = True

    def getElapsedTime(self):
        time_format = gst.Format(gst.FORMAT_TIME)
        try:
            elapsedTime = self.player.query_position(time_format, None)[0]
            return elapsedTime / 1000000
        except gst.QueryError:
            return 0


    def togglePause(self):
        if self.paused:
            self.paused = False
            self.player.set_state(gst.STATE_PLAYING)
        else:
            self.paused = True 
            self.player.set_state(gst.STATE_PAUSED)

    def onMessage(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.listener.finished()
        if t == gst.MESSAGE_ERROR:
            self.listener.finished()

    ##
    # Private callback function, you shouldn't touch this.
    def finished(self, data):
        self.listener.finished()


##
# This thread class listens to the Player and gives it a constant stream of music to play.
#
class PlayThread(threading.Thread):

    ##
    # Constructor.
    # @param player the Player object to give music to
    # @param playQueue The queue to take music from
    #
    def __init__(self, player, playQueue):
        threading.Thread.__init__(self)
        self.daemon = True
        self.player = player
        self.player.addListener(self)
        self.queue = playQueue
        self.condition = threading.Condition()
        self.listeners = list()
        
    ##
    # Called by thread.start, loops forever giving music to the Player
    def run(self):
        self.keepGoing = True
        self.condition.acquire()
        while self.keepGoing:
            item = self.queue.get()
            print("Playing: " + item.getDetails())
            self.player.playContent(item.getLocalPath())
            self.nowPlaying = item
            for l in self.listeners:
                l.itemPlaying(item)
            self.condition.wait()
        self.condition.release()

    ##
    # Callback function for the Player, gives it more music.
    def finished(self):
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()


    def stop(self):
        this.keepGoing = False
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()

    def addListener(self, listener):
        self.listeners.append(listener)
