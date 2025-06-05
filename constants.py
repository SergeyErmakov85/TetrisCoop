"""
Constants for the cooperative Tetris game
"""

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
CELL_SIZE = 25

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)
DARK_GRAY = (64, 64, 64)

# Piece colors
PIECE_COLORS = {
    'I': CYAN,
    'O': YELLOW,
    'T': PURPLE,
    'S': GREEN,
    'Z': RED,
    'J': BLUE,
    'L': ORANGE
}

# Player colors
PLAYER_1_COLOR = (100, 149, 237)  # Cornflower blue
PLAYER_2_COLOR = (255, 99, 71)    # Tomato red

# Game settings
FALL_TIME = 500  # milliseconds
FAST_FALL_TIME = 50  # milliseconds for fast drop
MOVE_DELAY = 100  # milliseconds between moves
ROTATION_DELAY = 150  # milliseconds between rotations

# Board position on screen
BOARD_X = 50
BOARD_Y = 50

# UI positions
SCORE_X = 300
SCORE_Y = 50
NEXT_PIECE_X = 400
NEXT_PIECE_Y = 100
PLAYER_INDICATOR_X = 300
PLAYER_INDICATOR_Y = 150

# Controls for Player 1
PLAYER_1_CONTROLS = {
    'left': 'a',
    'right': 'd',
    'down': 's',
    'rotate': 'w',
    'drop': 'q',
    'pass': 'e'
}

# Controls for Player 2
PLAYER_2_CONTROLS = {
    'left': 'j',
    'right': 'l',
    'down': 'k',
    'rotate': 'i',
    'drop': 'u',
    'pass': 'o'
}
