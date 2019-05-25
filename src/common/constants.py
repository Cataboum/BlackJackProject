# -*- coding: utf-8 -*-

# ============================================================================
# = File containing all the constant variables
# ============================================================================

import os
import json
from enum import Enum

from src.CardsAPI.Hand import Hand

# ============================================================================
# = Configuration parameters
# ============================================================================

__tmp = "data/config/path.cfg.json"
with open(__tmp, "r", encoding="utf-8") as f:
    CONFIG_PATH = json.load(f)
__tmp = "data/config/pictures.cfg.json"
with open(__tmp, "r", encoding="utf-8") as f:
    CONFIG_PICTURES = json.load(f)
__tmp = "data/config/menu.cfg.json"
with open(__tmp, "r", encoding="utf-8") as f:
    CONFIG_MENU = json.load(f)
__tmp = "data/config/game.cfg.json"
with open(__tmp, "r", encoding="utf-8") as f:
    CONFIG_GAME = json.load(f)

# ============================================================================
# = Directories path
# ============================================================================

DIR_SRC = os.path.join(*CONFIG_PATH["folders"]["src"])  # Source files
DIR_DATA = os.path.join(*CONFIG_PATH["folders"]["data"])  # Data files
DIR_CONFIG = os.path.join(*CONFIG_PATH["folders"]["config"])  # Configuration files
DIR_PICTURES = os.path.join(*CONFIG_PATH["folders"]["pictures"])  # Pictures

# ============================================================================
# = Enum
# ============================================================================


class Game(Enum):
    """
    Class with all the states of the game
    """
    quit = 0
    menu = 1
    play = 2
    option = 3


class Decision(Enum):
    """
    Class with decisions regarding Hands
    """
    stand = "STAND"
    hit = "HIT"
    double = "DOUBLE"
    split = "SPLIT"


class Moves(Enum):
    """
    Class with moves possibilities
    """
    up = 0
    down = 1


class PlayerHand:
    """
    Hand list index for player hand
    """

    def __init__(self, hand: Hand = None,
                 hand_bet: int = 0, is_lock: bool = False):
        self.hand: Hand = hand or Hand()
        self.hand_bet: int = hand_bet
        self.is_lock: bool = is_lock

    def __repr__(self):
        return (f"PlayerHand object(hand = {self.hand}, "
                f"hand_bet = {self.hand_bet}, "
                f"is_lock = {self.is_lock})")

    def __str__(self):
        return (f"{['', 'Locked'][self.is_lock]} "
                f"{self.hand} with bet: {self.hand_bet}")

# ============================================================================
# = Clear temporary variables
# ============================================================================

del __tmp
