from avonation.config import Config
from avonation.sint import Sint
class MainMenu:
    def __init__(self):
        self.sint = Sint()
        self.config = Config()
    #def pressSpace(self, itemMenu):
    #   self.sint.speak(itemMenu)
    def speak(self, itemMenu):
        self.sint.speak(self.config.listModes[itemMenu])
