import os

import pygame

from constants import DIRIMAGES


def load_image(filename: str) -> pygame.Surface:
    """
    Loads an image and prepares it

    :param filename: the path to the image
    :return: the image converted
    """

    try:
        surface = pygame.image.load(os.path.join(DIRIMAGES, filename))
    except pygame.error:
        error = "Could not load image \"%s\" %s" % (filename, pygame.get_error())
        raise SystemExit(error)

    return surface.convert()
