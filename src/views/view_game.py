import pygame
import src.common.constants as cst
from src.common.func_pictures import load_image, convert_card_to_picture
from src.CardsAPI.Card import Card
from collections import defaultdict


class View_game:

    def __init__(self, window, view_config):

        self.window = window
        self.view_config = view_config
        self.background = None  # init in init_window
        self.area_counts = defaultdict(int)

        self.init_window()

    def init_window(self):
        # Init the window with background
        bgd_tile = load_image("green_carpet.jpeg")
        bgd_tile = pygame.transform.scale(
            bgd_tile,
            (self.view_config["window"]["width"],
             self.view_config["window"]["height"])
        )
        self.background = pygame.Surface((self.view_config["window"]["width"],
                                          self.view_config["window"]["height"]))
        self.background.blit(bgd_tile, (0, 0))

        # Test the display of cards on the window
        self.add_card(Card('King'), "dealer")
        self.add_card(Card('Queen'), "dealer")

        # Display on windows
        self.window.blit(self.background, (0, 0))
        pygame.display.flip()

        # Init sprites
        all_sprites = pygame.sprite.RenderUpdates()

        # Update the scene
        dirty = all_sprites.draw(self.window)
        pygame.display.update(dirty)

    def add_card(self, card, area_name):
        card_area_config = self.view_config["card_areas"]
        area = card_area_config[area_name]

        offset = {k: v * self.area_counts[area_name] + 1
                  for k, v in card_area_config["extra_card_offset"].items()}

        pos = (area["x"] + offset["x"], area["y"] + offset["y"])
        self._add_card(card, pos)
        self.area_counts[area_name] += 1

    def _add_card(self, card, pos):
        """
        Add a card on the table view at a certain pos
        """
        card_tile = load_image(convert_card_to_picture(card))
        card_tile = pygame.transform.scale(
            card_tile,
            (cst.CONFIG_PICTURES['cards']['size']['width'],
             cst.CONFIG_PICTURES['cards']['size']['height'])
        )
        self.background.blit(card_tile, pos)

    def refresh(self):
        ...
