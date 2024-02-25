import pygame as pg

from src.config import CAPTION, ICON_PATH, resource_path
from src.main import App

pg.init()
pg.display.set_caption(CAPTION)

try:
    icon = pg.image.load(resource_path(ICON_PATH))
    pg.display.set_icon(icon)
except FileNotFoundError:
    pass

GameApp2048 = App()

def start() -> None:
    GameApp2048.run()