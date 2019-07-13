import copy
from typing import List

import pygame

from src.CardsAPI.Card import Card
from src.common.func_pictures import load_image, convert_card_to_picture
from src.common.game_view_config import game_view_config, Coordinates
from src.common.utils import Signal, SurfaceWithPosition


class CardAreaOrganizer:
    """
    Organizer class used to handle card placement for the view.
    Comes with a signal to tell the view we updated the cards to show.
    The add_card method is used to add a card to the organizer,
    which triggers the signal that tells the ViewGame class to refresh its
    view.
    """

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
        self.player_areas: List[List[SurfaceWithPosition]] = []

    def add_card(self, card: Card, human_type: str, area_id: int = None):
        """
        Generic method to add a Card to the organizer. Delegates to
        specialized methods depending on the parameters. Emits a signal to
        tell the ViewGame class to update the view
        :param Card card: the card we want to add to the organizer
        :param str human_type: either "dealer" or "player"
        :param int area_id: only for "player" human_type, specifies the id
        of the area to add the card to
        :return: None
        """
        card_tile = self.create_card_tile(card)
        if human_type == "dealer":
            self.add_dealer_card(card_tile)
        elif human_type == "player":
            if area_id is None:
                raise ValueError("Missing area_id for adding a player card")
            elif area_id > len(self.player_areas):
                raise ValueError("Wrong area_id for adding a player card")
            elif area_id == len(self.player_areas):
                self.add_new_player_area(card_tile, area_id)
            else:
                self.add_player_card(card_tile, area_id)
        else:
            raise ValueError(
                f"Unknown human type {human_type!r}, should be either "
                f'"dealer" or "player"'
            )
        self.areas_updated.emit()

    def split_hand(self, area_id):
        """
        Splits the hand designated by the area_id.
        The new created hand will be located on the right of the older one
        :param int area_id: the id of the area we want to split
        :return: None
        """
        areas_dict_ = {
            area: cards for area, cards in enumerate(self.player_areas)
        }
        self.player_areas = [[] for _ in range(len(self.player_areas) + 1)]

        areas_dict = {}

        for area, cards in areas_dict_.items():
            if area < area_id:
                areas_dict[area] = cards
            elif area == area_id:
                areas_dict[area] = [cards[0]]
                areas_dict[area + 1] = [cards[1]]
            else:
                areas_dict[area + 1] = cards

        for area, cards in areas_dict.items():
            for card in cards:
                self.add_player_card(card, area)

        self.areas_updated.emit()

    def add_dealer_card(self, card_tile):
        """
        Adds the card to self.dealer_area
        :param pygame.Surface card_tile: the image representing the card
        :return: None
        """
        x_offset = self.extra_card_offset.x * len(self.dealer_area)
        y_offset = self.extra_card_offset.y * len(self.dealer_area)

        x_pos = self.dealer_card_area_config.x + x_offset
        y_pos = self.dealer_card_area_config.y + y_offset

        position = Coordinates(x=x_pos, y=y_pos)

        self.dealer_area.append(SurfaceWithPosition(card_tile, position))

    def add_player_card(self, card_tile: pygame.Surface, area_id: int):
        """
        Adds the card to self.player_areas
        :param pygame.Surface card_tile: the image representing the card
        :param int area_id: id of the area to which we want to add the card
        :return: None
        """
        position = self.compute_player_area_position(area_id)
        self.player_areas[area_id].append(
            SurfaceWithPosition(card_tile, position)
        )

    def add_new_player_area(self, card_tile, area_id):
        """
        Called when adding a new card to a new player area. Since we add an
        area, we will need to re-compute position for all the already placed
        cards
        :param pygame.Surface card_tile: the image representing the new card
        :param int area_id: id of the new area to which we want to add the
        card to
        :return: None
        """
        areas_dict = {
            area: cards for area, cards in enumerate(self.player_areas)
        }
        self.player_areas = [[] for _ in range(len(self.player_areas) + 1)]

        for area, cards in areas_dict.items():
            for card in cards:
                self.add_player_card(card, area)

        self.add_player_card(card_tile, area_id)

    def compute_player_area_position(self, area_id: int) -> Coordinates:
        """
        Utility function, side-effect-free, used to compute the coordinates
        of the card to show, accounting for area id and the offset due to
        already present cards
        :param int area_id: id of the area to which we want to add the card
        :return Coordinates: Coordinates object containing x and y
        coordinates used to show the card tile onto the window
        """
        x_offset = self.extra_card_offset.x * len(self.player_areas[area_id])
        y_offset = self.extra_card_offset.y * len(self.player_areas[area_id])

        num_areas = len(self.player_areas)
        player_area_width = self.player_card_area_config.width

        x_pos = round(
            self.player_card_area_config.x +
            (player_area_width / (1 + num_areas)) * (area_id + 1)
        ) + x_offset
        y_pos = self.player_card_area_config.y + y_offset

        return Coordinates(x_pos, y_pos)

    @classmethod
    def create_card_tile(cls, card: Card) -> pygame.Surface:
        """
        Utility side-effect-free staticmethod. Loads the image corresponding
        to the card and scale it
        :param Card card: the card we want to load the image for
        :return pygame.Surface: The image of the card, loaded and scaled
        """
        card_image = load_image(convert_card_to_picture(card))
        card_tile = pygame.transform.scale(
            card_image, (cls.card_width, cls.card_height)
        )
        return card_tile
