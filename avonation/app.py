import curses
import curses.ascii
from os import system, environ
from os.path import join, expanduser, exists
import sys
from signal import signal, SIGINT, SIGTERM
from avonation.action import Action
from avonation.player import Player
from avonation.radio import Radio
from avonation.podcast import Podcast
from avonation.youtube import Youtube
class App:
    listModes = ['mainMenu', 'player', 'radio', 'podcast', 'youtube']
    selectMode = 0
    activeMode = 0
    def __init__(self, screen):
        self.action = Action()
        self.player = Player()
        self.radio = Radio()
        self.podcast = Podcast()
        self.youtube = Youtube()
        signal(SIGINT, self.shutdown)
        signal(SIGTERM, self.shutdown)
        self.screen = screen
        self.screen.keypad(1)
        curses.curs_set(0)
        curses.noecho()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)

    def run(self):
        self.input_loop()

    def input_loop(self):
        while True:
            try:
                char_ord = self.screen.getch()
                char = chr(char_ord)
                if char.upper() == 'Q' or char_ord == curses.ascii.ESC:  # Esc or Q
                    self.player.quitPlayer()
                    self.shutdown()
                elif char.upper() == 'I' or char_ord == curses.KEY_UP:  # Up or I
                    self.action.pressKeyUp(self)
                elif char.upper() == 'K' or char_ord == curses.KEY_DOWN:  # Down or K
                    self.action.pressKeyDown(self)
                elif char.upper() == 'J' or char_ord == curses.KEY_LEFT:  # J or Left
                    self.action.pressKeyLeft(self)
                elif char_ord == curses.ascii.LF or char.upper() == 'L' or char.upper() == ' ' or char_ord == curses.KEY_RIGHT:  # Enter, L, p or Right
                    self.action.pressEnter(self)
                elif char.upper() == '-':  # -
                    self.player.decreseVolume()
                elif char.upper() == '+' or char.upper() == '=':  # + or =
                    self.player.increseVolume()
            except Exception as e:
                print('Invalid keypress detected.')
                print(e)

    def display(self, text):
        self.screen.clear()
        self.screen.addstr(0, 0, text)
        self.screen.refresh()

    def shutdown(self):
        self.screen.keypad(0)
        curses.curs_set(1)
        curses.echo()
        curses.endwin()
        sys.exit(0)
