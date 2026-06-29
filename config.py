from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
FULLSCREEN = True
FPS = 60

GRID_ROWS = 4
GRID_COLS = 4
CARD_SIZE = 170
CARD_GAP = 22
GRID_TOP = 170

FLIP_BACK_DELAY_MS = 1000

BACKGROUND_COLOR = (9, 6, 18)
PANEL_COLOR = (20, 14, 34)
PANEL_BORDER_COLOR = (67, 49, 105)
TEXT_COLOR = (235, 233, 241)
MUTED_TEXT_COLOR = (166, 160, 184)
PRIMARY_COLOR = (76, 52, 128)
DANGER_COLOR = (126, 48, 78)
CARD_BORDER_COLOR = (93, 72, 138)
MATCHED_BORDER_COLOR = (184, 151, 255)

FONT_NAME = "verdana"

IMAGE_SET_TITLES = {
    "characters": "The boys",
    "memes": "Memes",
    "animals": "Jerk horse",
    "set4": "Mister Ptiza",
    "set5": "Platina disks",
    "set6": "Dwayne Djonson",
}
