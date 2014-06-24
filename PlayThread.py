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



import threading 

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
        self.player = player
        self.player.addListener(self)
        self.queue = playQueue
        self.condition = threading.Condition()
        

    ##
    # Called by thread.start, loops forever giving music to the Player
    def run(self):
        self.condition.acquire()
        while True:
            item = self.queue.get()
            print "Playing: " + item.getDetails()
            self.player.playContent(item.getLocalPath())
            self.condition.wait()
        self.condition.release()



    ##
    # Callback function for the Player, gives it more music.
    def finished(self):
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()


