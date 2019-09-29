import os

import pygame

from src.common.config import ConfigPath


def load_image(filename):
    """
    Loads an image, prepares it for play
    """

    filename = os.path.join(ConfigPath.folder("pictures"), filename)
    try:
        surface = pygame.image.load(filename)
    except pygame.error:
        error = f"Could not load image \"{filename}\" {pygame.get_error()}"
        raise SystemExit(error)
    return surface.convert_alpha()


def convert_card_to_picture(card):
    """
    Return the picture name of a Card object
    """
    if card.value == 1:
        value_name = "ACE"
    elif card.value != 10 or card.name == "TEN":
        value_name = str(card.value)
    else:
        value_name = card.name.lower()
    color = card.color.lower()

    card_picture_name = "%s_of_%s.png" % (value_name, color)
    return os.path.join('cards', card_picture_name)
