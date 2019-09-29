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

        # Buttons
        self.buttons = dict()

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

        disp = (
            ("card", "Carte", (100, 610)),
            ("bet", "Bet", (300, 610)),
            ("end_turn", "End Turn", (500, 610)),
            ("split", "Split", (700, 610)),
            ("double", "Double", (900, 610)),
            ("quit", "Quit", (900, 610))
        )
        for i, (iid, text, pos) in enumerate(disp):
            text = f"(i) {text}"
            b = Button(
                self.window, text=text, pos=pos, size=(100, 80), bg_normal=(180, 180, 180)
            )
            b.draw()
            self.buttons[iid] = b

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
