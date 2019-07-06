# ============================================================================
# =
# = Imports
# =
# ============================================================================

import os
import json
import time

import pygame
from pygame.locals import (
    QUIT,
    KEYDOWN,
    K_ESCAPE,
)

from src.common.constants import (
    Game,
    CONFIG_MENU,
    DIR_CONFIG,
    DIR_SRC,
    DIR_DATA,
    DIR_PICTURES,
)
from src.common.game_view_config import game_view_config
from src.views import view_menu, view_game, view_option
from src.controller.game_controller import GameController
from src.humans.Player import Player
# ============================================================================
# =
# = Application
# =
# ============================================================================


class Main:
    """
    The main application
    """

    def __init__(self):

        # Configuration
        self.loadConfig()

        # Init pygame
        self.initPygame()
        self.initController()

        # mainloop
        self.mainloop()

    def loadConfig(self):
        """
        Load the configuration file
        """

        file_config = os.path.join(DIR_CONFIG, "ui.cfg.json")

    def initPygame(self):
        """
        Initialize the main screen
        """

        pygame.init()
        pygame.display.set_caption("Black Jack by Hackiflette")
        self.game_window = pygame.display.set_mode((
            game_view_config.window.width,
            game_view_config.window.height,
        ))
        self.menu_window = pygame.display.set_mode((
            CONFIG_MENU["window"]["width"],
            CONFIG_MENU["window"]["height"],
        ))

    def initController(self):
        """
        Initialize the game_manager
        """

        self.ctrl = GameController(self.game_window)

    def mainloop(self):
        """
        The mainloop the launch the game
        """

        state, param = view_menu.main(
            self.menu_window, CONFIG_MENU["window"], CONFIG_MENU["menu_buttons"])

        while state != Game.quit:
            if state == Game.menu:
                self.ctrl.resetAllHumans()
                state, param = view_menu.main(
                    self.menu_window, CONFIG_MENU["window"], CONFIG_MENU["menu_buttons"])
            elif state == Game.play:
                self.ctrl.gameLaunch()
                state = self.gameLoop()
                # state, param = view_game.main(self.window, self.config["window"])
            elif state == Game.option:
                state, param = view_option.main(self.menu_window, CONFIG_MENU["window"])
            else:
                state = 0

        pygame.quit()

    def gameLoop(self):
        """
        The loop of the game which communicate with controller
        """
        state = Game.play
        print("GameLoop")
        while state == Game.play:
            for event in pygame.event.get():
                if event.type == QUIT:
                    state = Game.menu
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    state = Game.menu
                elif event.type:
                    keep_playing = self.ctrl.playOneRound()
                    if keep_playing == False :
                        #Player want to quit
                        state = Game.menu
        print("gameLoop")
        return state


if __name__ == '__main__':
    print("Exists?")
    for folder in [DIR_SRC, DIR_DATA, DIR_CONFIG, DIR_PICTURES]:
        print(folder, os.path.exists(folder))

    Main()
