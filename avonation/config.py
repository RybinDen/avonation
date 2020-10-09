import os, configparser
class Config():
    listModes = ['mainMenu', 'player', 'radio', 'podcast', 'youtube']
    configFile= '../config.ini'
    def __init__(self):
        if not os.path.isfile(self.configFile):
            self.create_config()

    def create_config(self): # Create a config file
        config = configparser.ConfigParser()
        section = "general"
        config.add_section(section)
        config.set(section, "language", "ru")
        config.set(section, "synthesizer", "espeak")
        section = "espeak"
        config.add_section(section)
        config.set(section, "speed", "200")
        config.set(section, "pitch", "50")
        config.set(section, "volume", "100")
        section = "rhvoice"
        config.add_section(section)
        config.set(section, "voice", "aleksandr")
        with open(self.configFile, "w") as config_file:
            config.write(config_file)

    def get_setting(self, section, setting): # Print out a setting
        config = configparser.ConfigParser()
        config.read(self.configFile)
        value = config.get(section, setting)
        return value

