



import pygst
pygst.require("0.10")
import gst
import os



class Player:
    
    def __init__(self):
        self.pipeline = gst.Pipeline("RadioPipe")
        self.player = gst.element_factory_make("playbin2", "player")
        self.fakesink = gst.element_factory_make("fakesink", "fakesink")
        self.output = gst.element_factory_make("alsasink", "audiosink")
        #self.output.set_property("device", "preview")
        self.player.set_property("video-sink", self.fakesink)
        self.player.set_property("audio-sink", self.output)
        self.pipeline.add(self.player)
        self.player.connect("about-to-finish", self.finished)


    def playContent(self, path):
        self.pipeline.set_state(gst.STATE_NULL)
        self.player.set_property("uri", "file://" + path)
        #self.player.set_property('uri', 'file://' + os.path.abspath('test.mp3'))
        self.pipeline.set_state(gst.STATE_PLAYING)

    def finished(self, data):
        print "finished"
