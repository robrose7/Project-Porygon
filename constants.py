import pygame

pygame.init()

# Ui Static Values
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

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

FONT_SMALL = pygame.font.Font(None, 30)
FONT_LARGE = pygame.font.Font(None, 60)

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