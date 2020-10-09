import evdev
from avonation.event import Event
from avonation.action import Action
from avonation.config import Config
from avonation.sint import Sint
from avonation.player import Player
from avonation.radio import Radio
from avonation.podcast import Podcast
from avonation.youtube import Youtube
class App:
    selectMode = 0
    activeMode = 0
    hello = 'hello'
    def __init__(self):
        self.config = Config()
        self.sint = Sint()
        self.event = Event()
        self.action = Action()
        self.player = Player()
        self.radio = Radio()
        self.podcast = Podcast()
        self.youtube = Youtube()
        self.device = self.getDevice()
    def getDevice(self):
        for fn in evdev.list_devices():
            device = evdev.InputDevice(fn)
            caps = device.capabilities()
            if evdev.events.EV_KEY in caps:
                if evdev.ecodes.KEY_1 in caps[evdev.events.EV_KEY]:
                   return device
        raise IOError('No keyboard found')

    def loop(self):
        for ev in self.device.read_loop():
            if ev.type == evdev.ecodes.EV_KEY:

                active = self.device.active_keys()
                if evdev.ecodes.KEY_LEFTCTRL in active and (evdev.ecodes.KEY_X in active or evdev.ecodes.KEY_C in active):
                   print('exit')
                   self.player.quitPlayer()           
                   break
                self.event.getKey(self, ev.code, ev.value)
