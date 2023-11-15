""" This file contains all the variables used in the game. """

from enum import Enum


RESOLUTION = (800, 600)
ZOOM = 1
UI_ZOOM = 2.0

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_GAP = 4


class GameStates(Enum):
    """The game states"""

    PLAYING = 0
    PAUSED = 1
    MENU = 2
    SAVING = 3
