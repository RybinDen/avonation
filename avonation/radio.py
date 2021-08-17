import curses
from os.path import join, expanduser, exists
class Radio:
    stationName = []
    station = [] #url
    stationNumber = 0 # current radiostation
    def __init__(self):
        self.radiostations_file_path = join(expanduser("~"), "radiostations")
        self.check_radiostations_exists()
        self.load_radios_list()

    def check_radiostations_exists(self):
        if not exists(self.radiostations_file_path):
            curses.endwin()
            print('No radiostations file detected at ' + self.radiostations_file_path + '. Aborting.')
            sys.exit(1)

    def load_radios_list(self):
        self.station = list()
        self.stationName = list()
        with open(self.radiostations_file_path) as radioList:
            for line in radioList.readlines():
                line = line.rstrip() # убрать с начала и конца пробельные символы, если они есть
                if len(line) == 0 or line[0] == ' ' or line[0] == '\t' or line.lstrip()[0] == '#':
                    continue
                try:
                    self.stationName.append(line.split("	")[0]) # 0 name, 1 url
                    self.station.append(line.split("	")[1]) # 0 name, 1 url
                except IndexError:
                    print('[-] Warning: Invalid format detected on line: %s' % line)

    def showRadiosList(self, app):
        app.screen.clear()
        num_header_rows = 2
        app.screen.addstr(0, 0, "Select radio (Press H for help):")
        for i, val in enumerate(self.radios):
            if i == self.stationNumber:
                app.screen.addstr(i + num_header_rows, 0, val, curses.color_pair(1) | curses.A_BOLD)
            else:
                app.screen.addstr(i + num_header_rows, 0, val)
        app.screen.addstr(23, 0, self.radios[self.current_station])
        app.screen.refresh()

    def launchPlayer(self):
        system("%s %s" % ('omxplayer', self.station[self.stationNumber]))
