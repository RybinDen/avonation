import os, glob
from omxplayer.player import OMXPlayer
class Player:
    player = None
    playing = False
    volume=0.5
    file = 'stub.mp3' # file playing
    files = []
    currentNumberFile = 0
    def __init__(self):
        self.totalObject = glob.glob('../*')
        for item in self.totalObject:
            if os.path.isdir(item):
                self.files.append(item)
        self.files  += glob.glob('../*.mp3')
        self.files  += glob.glob('../*.wav')
        self.countFiles = len(self.files)
        self.currentNumberFile = 0
        if self.playing == False:
            self.playFile(self.file)

    def quitPlayer(self):
        if self.player!=None:
            if self.playing != False:
                self.playing = False
            self.player.quit()

    def playerExit(self, code):
        self.playing=False
        self.player = None

    def playFile(self, fileName):
        if self.player==None:
            self.player=OMXPlayer(fileName)
            self.player.set_volume(self.volume)
            self.player.exitEvent += lambda _, exit_code: self.playerExit(exit_code)
        else:
            self.player.load(fileName)
        self.playing=True

    def increseVolume(self):
        if self.player!=None:
            if self.volume < 1:
                self.volume+=0.1
                self.player.set_volume(self.volume)

    def decreseVolume(self):
        if self.player!=None:
            if self.volume>0:
                self.volume-=0.1
                self.player.set_volume(self.volume)


