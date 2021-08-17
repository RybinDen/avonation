#console audio player for raspberry pi.
#version 1.0 update 16.08.2021
# Denis Rybin https://github.com/rybinden/avonation

import curses
from avonation.app import App

def main_wrapper(main_screen):
    app = App(main_screen)
    app.run()

curses.wrapper(main_wrapper)
