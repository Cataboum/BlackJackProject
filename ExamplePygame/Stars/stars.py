"""
This example is based on an official example.
It is located on the local directory of pygame:
site-package/pygame/examples/aliens.py

from pygame.examples.aliens import main
main()
"""

# ============================================================================
# =
# = Imports
# =
# ============================================================================

import os
import json

import pygame
from pygame.locals import *

# ============================================================================
# =
# = Functions
# =
# ============================================================================


def load_image(file):
    """
    Loads an image, prepares it for play
    """

    file = os.path.join(DIR_IMAGES, file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        error = "Could not load image \"%s\" %s" % (file, pygame.get_error())
        raise SystemExit(error)
    return surface.convert()

# ============================================================================
# =
# = Class
# =
# ============================================================================


class Star(pygame.sprite.Sprite):
    """
    A shooting star
    """

    speed = 2
    images = list()

    def __init__(self, **kwargs):
        """
        kwargs is used to define where the rect is places
        """
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(**kwargs)

    def update(self):
        """
        Update the star at each iteration
        """
        self.rect.move_ip(self.speed, 0)
        if not SCREENRECT.contains(self.rect):
            self.kill()

# ============================================================================
# =
# = Variables
# =
# ============================================================================

# ============================================================================
# = Environement
# ============================================================================


DIR_MAIN = os.path.dirname(__file__)
DIR_FILES = os.path.join(DIR_MAIN, "files")
DIR_IMAGES = os.path.join(DIR_MAIN, "images")

FILE_CONFIG = os.path.join(DIR_FILES, "config.json")

# ============================================================================
# = Load files
# ============================================================================

with open(FILE_CONFIG, "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

SCREENRECT = Rect(0, 0, *CONFIG["screen"]["size"])

# ============================================================================
# =
# = Main
# =
# ============================================================================


def main():
    """
    The main function
    """

    # Init pygame and screen
    pygame.init()
    screen = pygame.display.set_mode(SCREENRECT.size)
    # pygame.mouse.set_visible(False)

    # Load images, sounds and init the star object
    img = load_image(CONFIG["images"]["star"])
    Star.images = [img, pygame.transform.flip(img, 1, 0)]
    star_sound = pygame.mixer.Sound("sounds/boom.wav")

    # Load the background and diisplay it on screen
    bgdtile = load_image(CONFIG["images"]["background"])
    background = pygame.Surface(SCREENRECT.size)
    for x in range(0, SCREENRECT.width, bgdtile.get_width()):  # from, to, step
        background.blit(bgdtile, (x, 0))
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Init sprites
    star = pygame.sprite.Group()
    all_sprites = pygame.sprite.RenderUpdates()
    star_last = pygame.sprite.GroupSingle()

    Star.containers = star, all_sprites, star_last

    # Init the loop
    clock = pygame.time.Clock()
    Star(midleft=SCREENRECT.midleft)

    loop = True
    while loop:

        # clear/erase the last drawn sprites
        all_sprites.clear(screen, background)
        all_sprites.update()

        # Check for events
        for event in pygame.event.get():
            if event.type == QUIT:
                loop = False
            elif (event.type == KEYDOWN and event.key == K_ESCAPE):
                loop = False
            if event.type == pygame.MOUSEBUTTONUP:
                star_sound.play()
                pos = pygame.mouse.get_pos()
                Star(center=pos)

        # draw the scene
        dirty = all_sprites.draw(screen)
        pygame.display.update(dirty)

        clock.tick(40)
    # end while loop

    pygame.quit()

# ============================================================================
# =
# = Main
# =
# ============================================================================


if __name__ == '__main__':
    main()
