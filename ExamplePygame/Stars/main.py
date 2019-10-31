import os
import json

import pygame
from pygame.locals import *

from constants import *
from screen_splash import screen_splash
from screen_mainmenu import screen_mainmenu
from screen_play import screen_play


class Main:
    """
    The main application
    """

    def __init__(self):

        # Configuration
        self.load_config()

        # Init pygame
        self.init_pygame()

        # mainloop
        self.mainloop()

    def load_config(self):
        """
        Load the configuration file
        """

        fileConfig = os.path.join(DIRFILES, "config.json")
        with open(fileConfig, "r", encoding="utf-8") as f:
            self.config = json.load(f)

    def init_pygame(self):
        """
        Intialize the main screen
        """

        size = self.config["screen"]["size"]
        self.screenRect = Rect(0, 0, *size)

        pygame.init()
        pygame.font.init()

        self.window = pygame.display.set_mode(self.screenRect.size)

    def mainloop(self):
        """
        The mainloop the launch the game
        """

        state, param = screen_splash(self.window)

        while state != ENUM.quit:

            ENUM.print(state)

            if state == ENUM.mainmenu:
                state, param = screen_mainmenu(self.window, param)

            elif state == ENUM.play:
                param["config"] = self.config
                param["screenRect"] = self.screenRect
                state, param = screen_play(self.window, param)

            else:
                state = ENUM.quit

        pygame.quit()


if __name__ == '__main__':
    Main()
