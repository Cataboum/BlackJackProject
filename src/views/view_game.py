from collections import defaultdict
from typing import List

import pygame

from src.Button import Button
from src.CardsAPI.Card import Card
from src.common.func_pictures import load_image, convert_card_to_picture
from src.common.game_view_config import game_view_config, Coordinates
from src.common.utils import Signal, SurfaceWithPosition


class CardAreaOrganizer:
    dealer_card_area_config = game_view_config.card_areas.dealer
    player_card_area_config = game_view_config.card_areas.player
    extra_card_offset = game_view_config.card_areas.extra_card_offset
    card_width = game_view_config.cards.width
    card_height = game_view_config.cards.height
    window_width = game_view_config.window.width
    window_height = game_view_config.window.height

    def __init__(self):
        self.areas_updated = Signal()
        self.dealer_area: List[SurfaceWithPosition] = []
        self.player_areas: List[List[SurfaceWithPosition]] = [[]]

    def addCard(self, card, human_type, area_id=None):
        card_tile = self.createCardTile(card)
        if human_type == "dealer":
            self.addDealerCard(card_tile)
        elif human_type == "player":
            if area_id is None:
                raise ValueError("Missing area_id for adding a player card")
            self.addPlayerCard(card_tile, area_id)
        else:
            raise ValueError(
                f"Unknown human type {human_type!r}, should be either "
                f"\"dealer\" or \"player\""
            )
        self.areas_updated.emit()

    def addDealerCard(self, card_tile):
        x_offset = self.extra_card_offset.x * len(self.dealer_area)
        y_offset = self.extra_card_offset.y * len(self.dealer_area)

        x_pos = self.dealer_card_area_config.x + x_offset
        y_pos = self.dealer_card_area_config.y + y_offset

        position = Coordinates(x=x_pos, y=y_pos)

        self.dealer_area.append(SurfaceWithPosition(card_tile, position))

    def addPlayerCard(self, card_tile, area_id):
        x_offset = self.extra_card_offset.x * len(self.player_areas[area_id])
        y_offset = self.extra_card_offset.y * len(self.player_areas[area_id])

        position = self.computePlayerAreaPosition(area_id, x_offset, y_offset)
        self.player_areas[area_id].append(
            SurfaceWithPosition(card_tile, position)
        )

    def computePlayerAreaPosition(self, area_id, x_offset, y_offset):
        num_areas = len(self.player_areas)
        player_area_width = (
            self.player_card_area_config.width
        )

        x_pos = round(
            self.player_card_area_config.x +
            player_area_width / (1 + num_areas)
        )
        y_pos = self.player_card_area_config.y

        return Coordinates(x_pos, y_pos)

    @classmethod
    def createCardTile(cls, card):
        card_image = load_image(convert_card_to_picture(card))
        card_tile = pygame.transform.scale(
            card_image,
            (cls.card_width,
             cls.card_height)
        )
        return card_tile


class ViewGame:
    def __init__(self, window):
        self.window = window
        self.background = None  # init in init_window
        self._area_counts = defaultdict(int)
        self.card_area_organizer = CardAreaOrganizer()

        self.organizers = (
            self.card_area_organizer,
        )

        self.subscribe_to_organizers()

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
        self.card_area_organizer.addCard(Card("KING"), "dealer")
        self.card_area_organizer.addCard(Card("QUEEN"), "dealer")

        self.card_area_organizer.addCard(Card("ACE", "SPADES"), "player", 0)

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

    def add_card(self, card, area_name):
        card_area_config = game_view_config.card_areas
        area = getattr(card_area_config, area_name)

        n_cards = self._area_counts[area_name]

        offset = card_area_config.extra_card_offset

        pos = (area.x + n_cards * offset.x, area.y + n_cards * offset.y)
        self._add_card(card, pos)
        self._area_counts[area_name] += 1

    def _add_card(self, card, pos):
        """
        Add a card on the table view at a certain pos
        """
        card_tile = load_image(convert_card_to_picture(card))
        card_tile = pygame.transform.scale(
            card_tile,
            (game_view_config.cards.width,
             game_view_config.cards.height)
        )
        self.background.blit(card_tile, pos)

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
