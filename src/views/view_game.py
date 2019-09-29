from collections import defaultdict

import pygame

from src.button import Button
from src.cards.card import Card
from src.common.func_pictures import load_image
from src.common.game_view_config import game_view_config
from src.views.card_area_organizer import CardAreaOrganizer
from src.views.image_loaders.tokensloader import TokensLoader


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
            bgd_tile, (game_view_config.window.width, game_view_config.window.height)
        )
        self.background = pygame.Surface(
            (game_view_config.window.width, game_view_config.window.height)
        )
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
        pygame.draw.rect(
            self.window,
            cfg_btns.color,
            (cfg_btns.x, cfg_btns.y, cfg_btns.width, cfg_btns.height),
        )
        self.quit_btn = Button(
            pos=(1100, 610),
            width=80,
            height=80,
            text="(6) Quit",
            background=(180, 180, 180),
        )
        self.carte_btn = Button(
            pos=(100, 610),
            width=100,
            height=80,
            text="(1) Carte",
            background=(180, 180, 180),
        )
        self.bet_btn = Button(
            pos=(300, 610),
            width=100,
            height=80,
            text="(2) Bet",
            background=(180, 180, 180),
        )
        self.pass_btn = Button(
            pos=(500, 610),
            width=100,
            height=80,
            text="(3) End Turn",
            background=(180, 180, 180),
        )
        self.split_btn = Button(
            pos=(700, 610),
            width=100,
            height=80,
            text="(4) Split",
            background=(180, 180, 180),
        )
        self.double_btn = Button(
            pos=(900, 610),
            width=100,
            height=80,
            text="(5) Double",
            background=(180, 180, 180),
        )
        self.carte_btn.display(self.window)
        self.bet_btn.display(self.window)
        self.pass_btn.display(self.window)
        self.split_btn.display(self.window)
        self.double_btn.display(self.window)
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

        # TODO: Tokens should be resized and transparent
        token = TokensLoader.get_image(10)
        token = pygame.transform.scale(
            token, (game_view_config.tokens.width, game_view_config.tokens.height)
        )
        self.window.blit(token, (500, 300))

        # Update the scene
        scene = sprite_group.draw(self.window)
        pygame.display.flip()

        print("Updating View...Done!")
