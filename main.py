# ============================================================================
# =
# = Imports
# =
# ============================================================================

import os
from threading import Thread

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
from src.common.config import ConfigPath
from src.views import view_menu, view_option
from src.controller.game_controller import GameController
from src.tokens import Tokens


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

        # Init pygame
        self.game_window = None
        self.menu_window = None
        self.init_pygame()

        # Init GameController
        self.ctrl = GameController(self.game_window)

        # Needs Pygame initialization
        Tokens.initialize(ConfigPath.file("tokens"))

        # mainloop
        self.main_loop()

    def init_pygame(self):
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

    def main_loop(self):
        """
        The mainloop the launch the game
        """

        state, param = view_menu.main(
            self.menu_window, CONFIG_MENU["window"], CONFIG_MENU["menu_buttons"])

        while state != Game.quit:
            if state == Game.menu:
                self.ctrl.reset_all_humans()
                state, param = view_menu.main(
                    self.menu_window, CONFIG_MENU["window"], CONFIG_MENU["menu_buttons"])
            elif state == Game.play:
                self.ctrl.game_launch()
                state = self.game_loop()
                # state, param = view_game.main(self.window, self.config["window"])
            elif state == Game.option:
                state, param = view_option.main(self.menu_window, CONFIG_MENU["window"])
            else:
                state = 0

        pygame.quit()

    def game_loop(self):
        """
        The loop of the game which communicate with controller
        """
        state = Game.play
        print("GameLoop")

        # First Create Player
        self.ctrl.initiate_players()

        while state == Game.play:
            for event in pygame.event.get():
                if event.type == QUIT:
                    state = Game.menu
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    state = Game.menu
                elif event.type:
                    self.ctrl.first_round()
                    keep_playing = self.ctrl.play_one_round()
                    if not keep_playing:
                        # Player want to quit
                        state = Game.menu
        print("gameLoop")
        return state


if __name__ == '__main__':
    print("Exists?")
    for folder in [DIR_SRC, DIR_DATA, DIR_CONFIG, DIR_PICTURES]:
        print(folder, os.path.exists(folder))

    Main()
