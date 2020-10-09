import evdev
from avonation.sint import Sint

class Event:
    def __init__(self):
        self.sint = Sint()
    def getKey(self, app, code, value):
        if code ==  evdev.ecodes.KEY_ESC and value == 1:
            print('press escape key')
            #os.system('sudo shutdown -h now')

        if code ==  evdev.ecodes.KEY_T and value == 1:
            #print('speak time')
            self.sint.speakTime()
        
        if code ==  evdev.ecodes.KEY_D and value == 1:
            #print('speak date')
            self.sint.speakDate()

        if code ==  evdev.ecodes.KEY_1 and value == 1:
            print('decrese volume')
            app.player.decreseVolume()

        if code ==  evdev.ecodes.KEY_2 and value == 1:
            print('encrese volume')
            app.player.increseVolume()

        if code ==  evdev.ecodes.KEY_SPACE and value == 1:
            print('press space')
            app.action.pressKeySpace(app)

        if code ==  evdev.ecodes.KEY_ENTER and value == 1:
            print('press enter')
            app.action.pressKeyEnter(app)

        if code ==  evdev.ecodes.KEY_LEFT and value == 1:
            print('left')
            app.action.pressKeyLeft(app)

        if code ==  evdev.ecodes.KEY_RIGHT and value == 1:
            print('right')
            app.action.pressKeyRight(app)

        if code ==  evdev.ecodes.KEY_UP and value == 1:
            print('press ap')
            app.action.pressKeyUp(app)

        if code ==  evdev.ecodes.KEY_DOWN and value == 1:
            print('press down')
            app.action.pressKeyDown(app)
