import itertools
from typing import Dict, Tuple

import pygame

from src.cards.card import card_to_value_dict, colors
from src.common.func_pictures import load_card_image
from src.common.game_view_config import game_view_config


class CardsLoader:
    data: Dict[Tuple[str, str], pygame.Surface] = dict()
    card_width = game_view_config.cards.width
    card_height = game_view_config.cards.height

    @classmethod
    def initialize(cls):
        card_names = card_to_value_dict.keys()
        color_list = colors

        cards_tuples = itertools.product(card_names, color_list)

        # Convert key values as integer
        # And load images
        for card in cards_tuples:
            cls.data[card] = pygame.transform.scale(
                load_card_image(*card),
                (cls.card_width, cls.card_height)
            )

    @classmethod
    def get_image(cls, name: str, color: str) -> pygame.Surface:
        """
        Return the image corresponding to the value

        :param str name: card name
        :param str color: card color
        :return pygame.Surface: pygame surface object
        """

        return cls.data[(name, color)]
