import pygame
from pygame.locals import *

from class_star import Star
from func_images import load_image
from constants import *


def screen_play(window: pygame.Surface, param: dict = dict()) -> tuple:
    """
    The splash screen

    :param window: The main window where to display the game
    :param param: Some parameters from another screen
    :return: The state of the next screen and a dict with some parameters
    """

    state = ENUM.play
    config = param["config"]
    screenRect = param["screenRect"]

    # font = pygame.font.SysFont('Comic Sans MS', 30)
    # textSurface = font.render('Play', False, (255, 255, 255))

    # Load images, sounds and init the star object
    img = load_image(config["images"]["star"])
    Star.images = [img, pygame.transform.flip(img, 1, 0)]
    Star.screenRect = screenRect
    star_sound = pygame.mixer.Sound("sounds/boom.wav")

    # Load the background and diisplay it on screen
    bgdtile = load_image(config["images"]["background"])
    background = pygame.Surface(screenRect.size)
    for x in range(0, screenRect.width, bgdtile.get_width()):  # from, to, step
        background.blit(bgdtile, (x, 0))
    window.blit(background, (0, 0))

    pygame.display.flip()

    # Init sprites
    star = pygame.sprite.Group()
    all_sprites = pygame.sprite.RenderUpdates()
    star_last = pygame.sprite.GroupSingle()

    Star.containers = star, all_sprites, star_last

    # Init the loop
    clock = pygame.time.Clock()
    Star(midleft=screenRect.midleft)

    while state == ENUM.play:

        # clear/erase the last drawn sprites
        all_sprites.clear(window, background)
        all_sprites.update()

        # Check for events
        for event in pygame.event.get():
            if event.type == QUIT:
                state = ENUM.quit
            elif (event.type == KEYDOWN and event.key == K_ESCAPE):
                state = ENUM.quit
            elif (event.type == KEYDOWN and event.key == K_RETURN):
                state = ENUM.mainmenu

            if event.type == pygame.MOUSEBUTTONUP:
                star_sound.play()
                pos = pygame.mouse.get_pos()
                Star(center=pos)

        # draw the scene
        dirty = all_sprites.draw(window)
        pygame.display.update(dirty)

        clock.tick(40)

    return state, dict()
