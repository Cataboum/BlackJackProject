from collections import defaultdict

import pygame

from src.Button import Button
from src.CardsAPI.Card import Card
from src.common.func_pictures import load_image
from src.common.game_view_config import game_view_config
from src.views.card_area_organizer import CardAreaOrganizer


class ViewGame:
    def __init__(self, window):
        self._area_counts = defaultdict(int)

        # Organizers
        self.card_area_organizer = CardAreaOrganizer()
        self.organizers = (
            self.card_area_organizer,
        )

        self.subscribe_to_organizers()

        # Init Window
        self.window = window
        self.background = None  # init in init_window
        self.init_window()

    def subscribe_to_organizers(self):
        for organizer in self.organizers:
            organizer.areas_updated.attach(self.refresh)

    def init_window(self):
        # Init the window with background
        bgd_tile = load_image("green_carpet.jpeg")
        bgd_tile = pygame.transform.scale(
            bgd_tile,
            (game_view_config.window.width,
             game_view_config.window.height)
        )
        self.background = pygame.Surface((game_view_config.window.width,
                                          game_view_config.window.height))
        self.background.blit(bgd_tile, (0, 0))

        # Display on windows
        self.window.blit(self.background, (0, 0))

        self.init_game_btns()

        # Display everything
        pygame.display.flip()

        # Init sprites
        # all_sprites = pygame.sprite.Group()
        #
        # # Update the scene
        # dirty = all_sprites.draw(self.window)
        # pygame.display.update(dirty)
        self.card_area_organizer.add_card(Card("KING"), "dealer")
        self.card_area_organizer.add_card(Card("QUEEN"), "dealer")

        self.card_area_organizer.add_card(Card("ACE", "SPADES"), "player", 0)

    def init_game_btns(self):
        # Display game buttons area
        cfg_btns = game_view_config.game_buttons
        pygame.draw.rect(self.window, cfg_btns.color,
                         (cfg_btns.x, cfg_btns.y,
                          cfg_btns.width, cfg_btns.height))

        self.quit_btn = Button(pos=(1100, 610),
                               width=80,
                               height=80,
                               text='Quit',
                               background=(180, 180, 180))
        self.quit_btn.display(self.window)

    def refresh(self):
        print("Updating View...")
        # Init sprites
        sprite_group = pygame.sprite.Group()

        self.window.blit(self.background, (0, 0))
        self.init_game_btns()

        for el in self.card_area_organizer.dealer_area:
            self.window.blit(el.surface, el.position.as_tuple)
        for area in self.card_area_organizer.player_areas:
            for el in area:
                self.window.blit(el.surface, el.position.as_tuple)

        # Update the scene
        scene = sprite_group.draw(self.window)
        pygame.display.flip()

        print("Updating View...Done!")
