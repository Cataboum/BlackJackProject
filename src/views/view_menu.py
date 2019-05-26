# import os.path

import pygame
from pygame.locals import *
from typing import List

from src.common.constants import Game, Moves
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

    # Buttons
    btn_index = 0
    default_btn_format = {'color': (0, 0, 0),
                          'border': 0,
                          'border_color': (255, 255, 255),
                          'background': None}
    selected_btn_format = {'color': (255, 255, 255),
                           'border': 2,
                           'border_color': (255, 255, 255),
                           'background': (0, 170, 140)}

    def update_button_display(btn_index: int, btns_list: List[Button]):
        # Update button view according btn_index
        for btn in btns_list:
            btn.set(**default_btn_format)
        btns_list[btn_index].set(**selected_btn_format)

        # Update buttons display
        screen.blit(background, (0, 0))
        screen.blit(title_text, (80, 30))
        for btn in btns_list:
            btn.display(window)
        pygame.display.flip()

    def move_btn_index(move: Moves, btn_index: int, btns_list: List[Button]):
        # Change btn_index
        btn_index += move.value
        btn_index %= len(btns_list)

        update_button_display(btn_index, btns_list)

        return btn_index

    btn_play = Button(pos=(menu_buttons['play_btn']['x'], menu_buttons['play_btn']['y']),
                      width=200, height=50, text="Start (s)", value=Game.play)
    btn_options = Button(pos=(menu_buttons['option_btn']['x'], menu_buttons['option_btn']['y']),
                         width=200, height=50, text="Options (o)", value=Game.option)
    btn_quit = Button(pos=(menu_buttons['quit_btn']['x'], menu_buttons['quit_btn']['y']),
                      width=200, height=50, text="Quit (Esc)", value=Game.quit)

    btns_list = [btn_play, btn_options, btn_quit]
    update_button_display(btn_index, btns_list)

    # Display on windows
    screen.blit(background, (0, 0))
    screen.blit(title_text, (80, 30))
    for btn in btns_list:
        btn.display(window)

    pygame.display.flip()

    # Init sprites
    all_sprites = pygame.sprite.RenderUpdates()
    clock = pygame.time.Clock()

    state = Game.menu
    while state == Game.menu:

        # Clear all the sprites
        all_sprites.clear(screen, bgd_tile)
        all_sprites.update()

        # Check for events
        for event in pygame.event.get():
            if event.type == QUIT:
                state = Game.quit
            elif event.type == KEYDOWN and event.key == K_RETURN:
                # state = Game.play
                state = btns_list[btn_index].value
            elif event.type == KEYDOWN and event.key == K_s:
                state = Game.play
            elif event.type == KEYDOWN and event.key == K_o:
                state = Game.option
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                state = Game.quit

            elif event.type == KEYDOWN and event.key == K_DOWN:
                btn_index = move_btn_index(Moves.down, btn_index, btns_list)
            elif event.type == KEYDOWN and event.key == K_UP:
                btn_index = move_btn_index(Moves.up, btn_index, btns_list)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if btn_play.isClicked(pos):
                    btn_play.execute()

                    state = Game.play
                elif btn_options.isClicked(pos):
                    btn_options.execute()
                    state = Game.option
                elif btn_quit.isClicked(pos):
                    btn_quit.execute()
                    state = Game.quit

        # Update the scene
        dirty = all_sprites.draw(screen)
        pygame.display.update(dirty)

        clock.tick(40)

    return state, dict()
