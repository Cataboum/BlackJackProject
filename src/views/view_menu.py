# import os.path

import pygame
from pygame.locals import *
from typing import List

from src.common.constants import Game, Moves
from src.common.func_pictures import load_image

from src.button import Button

# TODO: Use a class instead of a function
def main(window: pygame.Surface, menu_config: dict):
    """ The main function of the view of menu"""

    # Init window
    state = Game.menu
    win_config = menu_config["window"]
    menu_buttons = menu_config["menu_buttons"]
    buttons_format = menu_config["menu_buttons_format"]

    # Load background image
    bgd_tile = load_image("green_carpet.jpeg")
    background = pygame.Surface((win_config["width"], win_config["height"]))
    background.blit(bgd_tile, (0, 0))

    # Prepare text
    title_font = pygame.font.Font(None, 44)
    title_text = title_font.render("Black Jack Project", 2, (255, 255, 255))

    # Buttons
    btn_index = 0
    default_btn_format = buttons_format["default"]
    selected_btn_format = buttons_format["selected"]

    def update_button_display(btn_index: int, btns_list: List[Button]):
        # Update button view according btn_index
        for btn in btns_list:
            btn.set(**default_btn_format)
        btns_list[btn_index].set(**selected_btn_format)

        # Update buttons display
        window.blit(background, (0, 0))
        window.blit(title_text, (80, 30))
        for btn in btns_list:
            btn.draw()
        pygame.display.flip()

    def move_btn_index(move: Moves, btn_index: int, btns_list: List[Button]):
        # Change btn_index
        btn_index += move.value
        btn_index %= len(btns_list)

        update_button_display(btn_index, btns_list)

        return btn_index
    
    def cmd_play_btn():
        nonlocal state
        state = Game.play
    
    def cmd_option_btn():
        nonlocal state
        state = Game.option
    
    def cmd_quit_btn():
        nonlocal state
        state = Game.quit
    
    disp = (
        ("play_btn", cmd_play_btn),
        ("option_btn", cmd_option_btn),
        ("quit_btn", cmd_quit_btn)
    )
    btns_list = list()
    for iid, cmd in disp:
        b = Button(
            window=window,
            text=menu_buttons[iid]["text"],
            pos=(menu_buttons[iid]["x"], menu_buttons[iid]["y"]),
            size=(menu_buttons[iid]["width"], menu_buttons[iid]["height"])
        )
        b.signal.attach(cmd)
        btns_list.append(b)

    update_button_display(btn_index, btns_list)

    # Display on windows
    window.blit(background, (0, 0))
    window.blit(title_text, (80, 30))
    for btn in btns_list:
        btn.draw()

    pygame.display.flip()

    # Init sprites
    all_sprites = pygame.sprite.RenderUpdates()
    clock = pygame.time.Clock()

    while state == Game.menu:

        # Clear all the sprites
        all_sprites.clear(window, bgd_tile)
        all_sprites.update()

        # Check for events
        for event in pygame.event.get():
            if event.type == QUIT:
                state = Game.quit
            elif event.type == KEYDOWN and event.key == K_RETURN:
                btns_list[btn_index].signal.emit()
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

            for btn in btns_list:
                btn.handle_event(event)

        # Update the scene
        dirty = all_sprites.draw(window)
        pygame.display.update(dirty)

        clock.tick(40)

    return state, dict()
