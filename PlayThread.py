


import threading 

class PlayThread(threading.Thread):

    def __init__(self, player, playQueue):
        threading.Thread.__init__(self)
        self.player = player
        self.player.addListener(self)
        self.queue = playQueue
        self.condition = threading.Condition()
        

    def run(self):
        self.condition.acquire()
        while True:
            item = self.queue.get()
            print "Playing: " + item.getDetails()
            self.player.playContent(item.getLocalPath())
            self.condition.wait()
        self.condition.release()



    def finished(self):
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()


