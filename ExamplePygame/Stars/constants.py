import os

from class_enum import Enum


DIRMAIN = os.path.dirname(__file__)
DIRFILES = os.path.join(DIRMAIN, "files")
DIRIMAGES = os.path.join(DIRMAIN, "images")
DIRSOUNDS = os.path.join(DIRMAIN, "sounds")


ENUM = Enum(
    "splash",
    "mainmenu",
    "play",
    "quit"
)
