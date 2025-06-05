"""
Tetris piece definitions and logic
"""
import random
from constants import PIECE_COLORS

class TetrisPiece:
    """Represents a Tetris piece with its shape, position, and rotation"""
    
    # Define all piece shapes (4 rotations each)
    SHAPES = {
        'I': [
            ['....', 'IIII', '....', '....'],
            ['..I.', '..I.', '..I.', '..I.'],
            ['....', '....', 'IIII', '....'],
            ['..I.', '..I.', '..I.', '..I.']
        ],
        'O': [
            ['OO', 'OO'],
            ['OO', 'OO'],
            ['OO', 'OO'],
            ['OO', 'OO']
        ],
        'T': [
            ['...', 'TTT', '.T.'],
            ['..T', '.TT', '..T'],
            ['...', '.T.', 'TTT'],
            ['.T.', 'TT.', '.T.']
        ],
        'S': [
            ['...', '.SS', 'SS.'],
            ['.S.', '.SS', '..S'],
            ['...', '.SS', 'SS.'],
            ['S..', 'SS.', '.S.']
        ],
        'Z': [
            ['...', 'ZZ.', '.ZZ'],
            ['..Z', '.ZZ', '.Z.'],
            ['...', 'ZZ.', '.ZZ'],
            ['.Z.', 'ZZ.', 'Z..']
        ],
        'J': [
            ['...', 'JJJ', '..J'],
            ['..J', '..J', '.JJ'],
            ['...', 'J..', 'JJJ'],
            ['.JJ', '.J.', '.J.']
        ],
        'L': [
            ['...', 'LLL', 'L..'],
            ['..L', '..L', '..L'],
            ['...', '..L', 'LLL'],
            ['.L.', '.L.', '.LL']
        ]
    }
    
    def __init__(self, piece_type=None, x=4, y=0):
        """Initialize a new piece"""
        if piece_type is None:
            piece_type = random.choice(list(self.SHAPES.keys()))
        
        self.type = piece_type
        self.x = x
        self.y = y
        self.rotation = 0
        self.color = PIECE_COLORS[piece_type]
        self.shape = self.SHAPES[piece_type][self.rotation]
    
    def get_shape(self):
        """Get the current shape based on rotation"""
        return self.SHAPES[self.type][self.rotation]
    
    def get_cells(self):
        """Get all occupied cells of the piece"""
        cells = []
        shape = self.get_shape()
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell != '.' and cell != ' ':
                    cells.append((self.x + col_idx, self.y + row_idx))
        return cells
    
    def move(self, dx, dy):
        """Move the piece by the given offset"""
        self.x += dx
        self.y += dy
    
    def rotate(self):
        """Rotate the piece clockwise"""
        self.rotation = (self.rotation + 1) % 4
    
    def copy(self):
        """Create a copy of this piece"""
        new_piece = TetrisPiece(self.type, self.x, self.y)
        new_piece.rotation = self.rotation
        return new_piece
    
    @staticmethod
    def get_random_piece():
        """Generate a random piece"""
        return TetrisPiece()
    
    def get_width(self):
        """Get the width of the current shape"""
        shape = self.get_shape()
        if not shape:
            return 0
        return len(shape[0])
    
    def get_height(self):
        """Get the height of the current shape"""
        shape = self.get_shape()
        return len(shape)
