import pygame
from pygame.locals import *

import src.common.constants as cst
from src.common.func_pictures import load_image


def main(window, menu_config):
    """ The main function of the view of options"""

    # Init window
    screen = window

    # Load background image
    bgd_tile = load_image("green_carpet.jpeg")
    background = pygame.Surface((menu_config["width"], menu_config["height"]))
    background.blit(bgd_tile, (0, 0))

    # Prepare text
    title_font = pygame.font.Font(None, 44)
    title_text = title_font.render("Options", 2, (255, 255, 255))

    # Display on windows
    screen.blit(background, (0, 0))
    screen.blit(title_text, (80, 30))
    pygame.display.flip()

    # Init sprites
    all_sprites = pygame.sprite.RenderUpdates()
    clock = pygame.time.Clock()

    state = cst.Game.option
    while state == cst.Game.option:

        # Clear all the sprites
        all_sprites.clear(screen, bgd_tile)
        all_sprites.update()

        # Check for events
        for event in pygame.event.get():
            if event.type == QUIT:
                state = cst.Game.menu
            elif (event.type == KEYDOWN and event.key == K_ESCAPE):
                state = cst.Game.menu

        # Update the scene
        dirty = all_sprites.draw(screen)
        pygame.display.update(dirty)

        clock.tick(40)

    return state, dict()
