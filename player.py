"""
Player management for cooperative Tetris
"""
import pygame
from tetris_pieces import TetrisPiece
from constants import PLAYER_1_CONTROLS, PLAYER_2_CONTROLS

class Player:
    """Represents a player in the cooperative Tetris game"""
    
    def __init__(self, player_id, color):
        """Initialize a player"""
        self.id = player_id
        self.color = color
        self.current_piece = None
        self.next_piece = TetrisPiece.get_random_piece()
        self.score = 0
        self.pieces_placed = 0
        self.lines_contributed = 0
        
        # Set controls based on player ID
        if player_id == 1:
            self.controls = PLAYER_1_CONTROLS
        else:
            self.controls = PLAYER_2_CONTROLS
        
        # Input timing
        self.last_move_time = 0
        self.last_rotation_time = 0
        self.move_delay = 100  # milliseconds
        self.rotation_delay = 150  # milliseconds
    
    def spawn_new_piece(self):
        """Spawn a new piece for this player"""
        self.current_piece = self.next_piece
        self.next_piece = TetrisPiece.get_random_piece()
        
        # Center the piece horizontally
        self.current_piece.x = 4
        self.current_piece.y = 0
    
    def can_move(self, current_time):
        """Check if enough time has passed since last move"""
        return current_time - self.last_move_time >= self.move_delay
    
    def can_rotate(self, current_time):
        """Check if enough time has passed since last rotation"""
        return current_time - self.last_rotation_time >= self.rotation_delay
    
    def handle_input(self, keys_pressed, current_time, game_board):
        """Handle player input and return action taken"""
        if not self.current_piece:
            return None
        
        action = None
        
        # Check for rotation
        if keys_pressed.get(self.controls['rotate'], False) and self.can_rotate(current_time):
            test_piece = self.current_piece.copy()
            test_piece.rotate()
            if game_board.is_valid_position(test_piece):
                self.current_piece.rotate()
                action = 'rotate'
                self.last_rotation_time = current_time
        
        # Check for movement
        if self.can_move(current_time):
            if keys_pressed.get(self.controls['left'], False):
                test_piece = self.current_piece.copy()
                test_piece.move(-1, 0)
                if game_board.is_valid_position(test_piece):
                    self.current_piece.move(-1, 0)
                    action = 'move_left'
                    self.last_move_time = current_time
            
            elif keys_pressed.get(self.controls['right'], False):
                test_piece = self.current_piece.copy()
                test_piece.move(1, 0)
                if game_board.is_valid_position(test_piece):
                    self.current_piece.move(1, 0)
                    action = 'move_right'
                    self.last_move_time = current_time
            
            elif keys_pressed.get(self.controls['down'], False):
                test_piece = self.current_piece.copy()
                test_piece.move(0, 1)
                if game_board.is_valid_position(test_piece):
                    self.current_piece.move(0, 1)
                    action = 'move_down'
                    self.last_move_time = current_time
        
        # Check for hard drop
        if keys_pressed.get(self.controls['drop'], False):
            drop_y = game_board.get_drop_position(self.current_piece)
            self.current_piece.y = drop_y
            action = 'hard_drop'
        
        # Check for pass piece
        if keys_pressed.get(self.controls['pass'], False):
            action = 'pass_piece'
        
        return action
    
    def add_score(self, points):
        """Add points to the player's score"""
        self.score += points
    
    def piece_placed(self):
        """Called when a piece is successfully placed"""
        self.pieces_placed += 1
        self.current_piece = None
    
    def receive_piece(self, piece):
        """Receive a piece from another player"""
        if self.current_piece is None:
            self.current_piece = piece
            self.current_piece.x = 4
            self.current_piece.y = 0
            return True
        return False
