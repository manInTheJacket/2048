from __future__ import annotations
# Importing necessary modules
from abc import abstractmethod

import pygame as pg

from src.config import Size

# Defining a class for the main attributes of the game
class Game:
    # Defining class attributes
    screen: pg.SurfaceType
    clock: pg.time.Clock
    framerate: int
    width: int
    height: int
    victory: bool
    username: str | None
    score: int
    old_score: int
    # Initializing the game object
    def __init__(self, size: Size, framerate: int = 60) -> None:
        # Setting up the game window
        self.screen = pg.display.set_mode((size.width, size.height))
        self.clock = pg.time.Clock()
        self.framerate = framerate
        self.width = size.width
        self.height = size.height
        # Initializing game attributes
        self.victory = False
        self.username = None
        self.score, self.old_score = 0, 0

    # Abstract method for updating the game status
    @abstractmethod
    def update(self) -> None:
        """Updating the game status."""
    # Abstract method for handling player input events
    @abstractmethod
    def handle_events(self) -> bool:
        """Handles actions entered by the player."""
    # Abstract method for running game
    @abstractmethod
    def run(self) -> None:
        """Launches the game."""
