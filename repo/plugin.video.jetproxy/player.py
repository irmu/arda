import xbmc

class ProxyPlayer(xbmc.Player):
    def __init__(self, server):
        xbmc.Player.__init__(self)
        self.server = server

    def onPlayBackEnded(self):
        if self.server != None:
            self.server.shutdown()

    def onPlayBackStarted(self):
        if self.server != None:
            self.server.shutdown()
    
    def onPlaybackStopped(self):
        if self.server != None:
            self.server.shutdown()