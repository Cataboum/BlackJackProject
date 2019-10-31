import pygame
from pygame.locals import *

from constants import *


def screen_mainmenu(window: pygame.Surface, param: dict = dict()) -> tuple:
    """
    The splash screen

    :param window: The main window where to display the game
    :param param: Some parameters from another screen
    :return: The state of the next screen and a dict with some parameters
    """

    state = ENUM.mainmenu

    font = pygame.font.SysFont('Comic Sans MS', 30)
    textSurface = font.render('Main Menu', False, (0, 0, 0))

    window.fill((0, 127, 127))
    window.blit(textSurface, (0, 0))

    while state == ENUM.mainmenu:

        # Check for events
        for event in pygame.event.get():
            if event.type == QUIT:
                state = ENUM.quit
            elif (event.type == KEYDOWN and event.key == K_ESCAPE):
                state = ENUM.quit
            elif (event.type == KEYDOWN and event.key == K_RETURN):
                state = ENUM.play

        pygame.display.flip()

    return state, dict()
