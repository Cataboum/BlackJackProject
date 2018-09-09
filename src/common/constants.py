# -*- coding: utf-8 -*-

# ============================================================================
# = File containing all the constant variables
# ============================================================================

import os
import json
from enum import Enum

# ============================================================================
# = Configuration parameters
# ============================================================================

__tmp = "data/config/path.cfg.json"
with open(__tmp, "r", encoding="utf-8") as f:
    CONFIG_PATH = json.load(f)
__tmp = "data/config/pictures.cfg.json"
with open(__tmp, "r", encoding="utf-8") as f:
    CONFIG_PICTURES = json.load(f)
__tmp = "data/config/ui.cfg.json"
with open(__tmp, "r", encoding="utf-8") as f:
    CONFIG_UI = json.load(f)

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
    stand = 0
    hit = 1
    double = 2
    split = 3

# ============================================================================
# = Clear temporary variables
# ============================================================================

del __tmp
