import pygame
import flags
pygame.init()

# Ui Static Values
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 1200

HP_BAR_WIDTH = 200
HP_BAR_HEIGHT = 20
HP_BAR_MARGIN = 10
HP_BAR_BORDER_WIDTH = 2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARK_GREEN = (17, 150, 52)

TYPE_COLORS = {
    0: (168, 168, 120),   # NORMAL
    1: (240, 128, 48),    # FIRE
    2: (104, 144, 240),   # WATER
    3: (120, 200, 80),    # GRASS
    4: (248, 208, 48),    # ELECTRIC
    5: (152, 216, 216),   # ICE
    6: (192, 48, 40),     # FIGHTING
    7: (160, 64, 160),    # POISON
    8: (224, 192, 104),   # GROUND
    9: (168, 144, 240),   # FLYING
    10: (248, 88, 136),   # PSYCHIC
    11: (168, 184, 32),   # BUG
    12: (184, 160, 56),   # ROCK
    13: (112, 88, 152),   # GHOST
    14: (112, 56, 248),   # DRAGON
    15: (112, 88, 72),    # DARK
    16: (184, 184, 208),  # STEEL
    17: (238, 153, 172)   # FAIRY
}

FONT_SMALL = pygame.font.Font(None, 30)
FONT_LARGE = pygame.font.Font(None, 60)

SINGLE_POKEMON_INDEX = 2

TURN_BUFFER = 1 if flags.ai_flag else 1000
NEW_GAME_BUFFER = 1 if flags.ai_flag else 1000

types = {
    'NORMAL': 0,
    'FIRE': 1,
    'WATER': 2,
    'GRASS': 3,
    'ELECTRIC': 4,
    'ICE': 5,
    'FIGHTING': 6,
    'POISON': 7,
    'GROUND': 8,
    'FLYING': 9,
    'PSYCHIC': 10,
    'BUG': 11,
    'ROCK': 12,
    'GHOST': 13,
    'DRAGON': 14,
    'DARK': 15,
    'STEEL': 16,
    'FAIRY': 17,
}

categories = {
    'PHYSICAL': 0,
    'SPECIAL': 1,
    'STATUS': 2,
}