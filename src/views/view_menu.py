# import os.path

import pygame
from pygame.locals import *

import src.common.constants as cst
from src.common.func_pictures import load_image

from src.Button import Button


def main(window: pygame.Surface, menu_config: dict, menu_buttons: dict):
    """ The main function of the view of menu"""

    # Init window
    screen = window

    # Load background image
    bgd_tile = load_image("green_carpet.jpeg")
    background = pygame.Surface((menu_config["width"], menu_config["height"]))
    background.blit(bgd_tile, (0, 0))

    # Prepare text
    title_font = pygame.font.Font(None, 44)
    title_text = title_font.render("Black Jack Project", 2, (255, 255, 255))

    # core_font = pygame.font.Font(None, 30)
    # begin_text = core_font.render('Start (Enter)', 2, (255, 255, 255))
    # option_text = core_font.render('Options (o)', 2, (255, 255, 255))
    # quit_text = core_font.render('Quit (Esc)', 2, (255, 255, 255))

    btn_play = Button(pos=(menu_buttons['play_btn']['x'], menu_buttons['play_btn']['y']),
                      width=200, height=50, text="Start (Enter)",
                      color=(255, 255, 255), border=2, border_color=(255, 255, 255),
                      background=(0, 170, 140))
    btn_options = Button(pos=(menu_buttons['option_btn']['x'], menu_buttons['option_btn']['y']),
                         width=200, height=50, text="Options (o)")
    btn_quit = Button(pos=(menu_buttons['quit_btn']['x'], menu_buttons['quit_btn']['y']),
                      width=200, height=50, text="Quit (Esc)")

    btn_play.set(command=lambda: print("Ok"))
    btn_options.set(command=lambda: print("Ok"))
    btn_quit.set(command=lambda: print("Ok"))

    # Display on windows
    screen.blit(background, (0, 0))
    screen.blit(title_text, (80, 30))
    # screen.blit(begin_text, (menu_buttons["play_btn"]["x"], menu_buttons["play_btn"]["y"]))
    # screen.blit(option_text, (menu_buttons["option_btn"]["x"], menu_buttons["option_btn"]["y"]))
    # screen.blit(quit_text, (menu_buttons["quit_btn"]["x"], menu_buttons["quit_btn"]["y"]))
    btn_play.display(window)
    btn_options.display(window)
    btn_quit.display(window)

    pygame.display.flip()

    # Init sprites
    all_sprites = pygame.sprite.RenderUpdates()
    clock = pygame.time.Clock()

    state = cst.Game.menu
    while state == cst.Game.menu:

        # Clear all the sprites
        all_sprites.clear(screen, bgd_tile)
        all_sprites.update()

        # Check for events
        for event in pygame.event.get():
            if event.type == QUIT:
                state = cst.Game.quit
            elif event.type == KEYDOWN and event.key == K_RETURN:
                state = cst.Game.play
            elif event.type == KEYDOWN and event.key == K_o:
                state = cst.Game.option
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                state = cst.Game.quit

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if btn_play.isClicked(pos):
                    btn_play.execute()

                    state = cst.Game.play
                elif btn_options.isClicked(pos):
                    btn_options.execute()
                    state = cst.Game.option
                elif btn_quit.isClicked(pos):
                    btn_quit.execute()
                    state = cst.Game.quit

        # Update the scene
        dirty = all_sprites.draw(screen)
        pygame.display.update(dirty)

        clock.tick(40)

    return state, dict()
