import sys
from pathlib import Path
from typing import NamedTuple

# Defines a function to get the absolute path of resources, works for both development and bundled applications.
def resource_path(relative_path: Path) -> Path:
    # Determine base path for the application, considering PyInstaller's temporary folder if the app is bundled.
    base_path = Path(getattr(sys, "_MEIPASS", ".")).absolute()
    # Join the base path with the relative path of the resource.
    return base_path.joinpath(relative_path)

# NamedTuple for storing size with width and height as integers.
Size = NamedTuple("Size", (("width", int), ("height", int)))

# Path to the application's directory.
APP_PATH = resource_path(Path(__file__).parent)

# Window size settings.
WIDTH, HEIGHT = 520, 725
SIZE = Size(width=WIDTH, height=HEIGHT)  # Window size as a named tuple.
CAPTION = "Inception to TTFE"  # Window caption or title.
FRAMERATE = 120  # Maximum frames per second.

# Game area settings.
BLOCKS = 4  # Number of blocks per row/column.
SIZE_BLOCK = 112  # Pixel size of each block.
MARGIN = 9  # Margin size between blocks.

USERNAME = None  # Variable for storing username, starts as None.
MIN_NAME_LENGTH = 3  # Minimum length for a valid username.

# Folder names for resources.
images_source_folder_name = "images"

bg_images_name = "BG"  # Background image folder name.
elements = "elements"  # Game elements folder name.

icon_name = "icon.png"  # Application icon file name.
icon_folder_name = "icons"  # Folder name for icons.

# Paths to specific resources using the resource_path function.
ICON_PATH = resource_path(Path(images_source_folder_name) / Path(icon_folder_name) / Path(icon_name))
BG_PATH = resource_path(Path(images_source_folder_name) / Path(bg_images_name))
ELEMENTS_PATH = resource_path(Path(images_source_folder_name) / Path(elements))

GENERAL_FONT = APP_PATH / "vag-world-bold.ttf"  # The main font used in the game.

# A dictionary of color codes used in the game, with keys as numbers for number blocks or specific rows.
COLORS = {
    0: "#2e2e2e",
    2: "#3d2626",
    4: "#4e2020",
    8: "#600000",
    16: "#7a1a1a",
    32: "#8b0000",
    64: "#9f1e20",
    128: "#a22828",
    256: "#ab3232",
    512: "#b33d3d",
    1024: "#bf4747",
    2048: "#cb5151",
    "WHITE": "#ebeeff",  # Color for text.
    "GRAY": "#aebad0",  # Color for text.
    "BLACK": "#000000"
}