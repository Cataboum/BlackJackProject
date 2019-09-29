import os

import pygame

from src.common.config import ConfigPath
from src.cards.card import card_to_value_dict


def load_card_image(name: str, color: str) -> pygame.Surface:
    """
    From a Card object, compute its path and loads the corresponding image
    :param str name: value of the card to be loaded
    :param color: value of the card to be loaded
    :return pygame.Surface: pygame surface
    """
    return load_image(convert_card_to_picture_path(name, color))


def load_image(path: str) -> pygame.Surface:
    """
    Loads an image
    :param path: path of the object to be loaded
    :return pygame.Surface:
    """

    filename = os.path.join(ConfigPath.folder("pictures"), path)
    try:
        surface = pygame.image.load(filename)
    except pygame.error:
        e = OSError(
            f"Could not load image \"{filename}\" {pygame.get_error()}"
        )
        raise e
    return surface.convert_alpha()


def convert_card_to_picture_path(name: str, color: str) -> str:
    """
    Return the picture name of a Card object
    """
    if name.upper() not in ("ACE", "JACK", "QUEEN", "KING"):
        name = str(card_to_value_dict[name])

    color = color.lower()

    card_picture_name = "%s_of_%s.png" % (name, color)
    return os.path.join('cards', card_picture_name)
