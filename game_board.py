"""
Game board management for cooperative Tetris
"""
from constants import BOARD_WIDTH, BOARD_HEIGHT, BLACK

class GameBoard:
    """Manages the Tetris game board state"""
    
    def __init__(self):
        """Initialize an empty game board"""
        self.grid = [[BLACK for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.lines_cleared = 0
        self.last_piece_player = None  # Track which player placed the last piece
    
    def is_valid_position(self, piece):
        """Check if a piece can be placed at its current position"""
        cells = piece.get_cells()
        for x, y in cells:
            # Check bounds
            if x < 0 or x >= BOARD_WIDTH or y >= BOARD_HEIGHT:
                return False
            # Check collision with existing blocks (only if y >= 0)
            if y >= 0 and self.grid[y][x] != BLACK:
                return False
        return True
    
    def place_piece(self, piece, player_id):
        """Place a piece on the board permanently"""
        cells = piece.get_cells()
        for x, y in cells:
            if 0 <= y < BOARD_HEIGHT and 0 <= x < BOARD_WIDTH:
                self.grid[y][x] = piece.color
        
        self.last_piece_player = player_id
        return self.clear_lines()
    
    def clear_lines(self):
        """Clear completed lines and return the number cleared"""
        lines_to_clear = []
        
        # Find completed lines
        for y in range(BOARD_HEIGHT):
            if all(cell != BLACK for cell in self.grid[y]):
                lines_to_clear.append(y)
        
        # Remove completed lines
        for y in sorted(lines_to_clear, reverse=True):
            del self.grid[y]
            self.grid.insert(0, [BLACK for _ in range(BOARD_WIDTH)])
        
        lines_cleared = len(lines_to_clear)
        self.lines_cleared += lines_cleared
        return lines_cleared
    
    def is_game_over(self):
        """Check if the game is over (top row has blocks)"""
        return any(cell != BLACK for cell in self.grid[0])
    
    def get_drop_position(self, piece):
        """Get the Y position where the piece would land if dropped"""
        test_piece = piece.copy()
        while self.is_valid_position(test_piece):
            test_piece.move(0, 1)
        test_piece.move(0, -1)
        return test_piece.y
    
    def get_height(self):
        """Get the height of the highest block on the board"""
        for y in range(BOARD_HEIGHT):
            if any(cell != BLACK for cell in self.grid[y]):
                return BOARD_HEIGHT - y
        return 0
    
    def clear_board(self):
        """Clear the entire board"""
        self.grid = [[BLACK for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.lines_cleared = 0
        self.last_piece_player = None
