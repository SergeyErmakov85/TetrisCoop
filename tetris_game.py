"""
Main game logic for cooperative Tetris
"""
import pygame
import time
from game_board import GameBoard
from player import Player
from tetris_pieces import TetrisPiece
from constants import *

class CooperativeTetris:
    """Main game class for cooperative Tetris"""
    
    def __init__(self):
        """Initialize the game"""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Cooperative Tetris")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.board = GameBoard()
        self.player1 = Player(1, PLAYER_1_COLOR)
        self.player2 = Player(2, PLAYER_2_COLOR)
        self.current_player = self.player1
        self.other_player = self.player2
        
        # Cooperative features
        self.shared_score = 0
        self.cooperation_bonus = 0
        self.turn_switch_timer = 0
        self.turn_duration = 10000  # 10 seconds per turn
        
        # Game timing
        self.last_fall_time = time.time() * 1000
        self.fall_time = FALL_TIME
        
        # Game state
        self.running = True
        self.game_over = False
        self.paused = False
        
        # Font for UI
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Initialize first pieces
        self.player1.spawn_new_piece()
        self.player2.spawn_new_piece()
        
        # Start with player 1
        self.switch_turn()
    
    def switch_turn(self):
        """Switch to the other player's turn"""
        if self.current_player == self.player1:
            self.current_player = self.player2
            self.other_player = self.player1
        else:
            self.current_player = self.player1
            self.other_player = self.player2
        
        self.turn_switch_timer = time.time() * 1000
        
        # If current player doesn't have a piece, spawn one
        if not self.current_player.current_piece:
            self.current_player.spawn_new_piece()
    
    def handle_events(self):
        """Handle pygame events"""
        keys_pressed = {}
        
        # Get currently pressed keys
        keys = pygame.key.get_pressed()
        
        # Map pygame keys to our control system
        key_map = {
            pygame.K_a: 'a', pygame.K_d: 'd', pygame.K_s: 's', 
            pygame.K_w: 'w', pygame.K_q: 'q', pygame.K_e: 'e',
            pygame.K_j: 'j', pygame.K_l: 'l', pygame.K_k: 'k',
            pygame.K_i: 'i', pygame.K_u: 'u', pygame.K_o: 'o'
        }
        
        for pygame_key, char in key_map.items():
            keys_pressed[char] = keys[pygame_key]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r and self.game_over:
                    self.restart_game()
                elif event.key == pygame.K_TAB:
                    # Manual turn switch
                    self.switch_turn()
        
        return keys_pressed
    
    def update_game_logic(self, keys_pressed):
        """Update game logic"""
        if self.paused or self.game_over:
            return
        
        current_time = time.time() * 1000
        
        # Check for turn timeout
        if current_time - self.turn_switch_timer > self.turn_duration:
            self.switch_turn()
        
        # Handle current player input
        if self.current_player.current_piece:
            action = self.current_player.handle_input(keys_pressed, current_time, self.board)
            
            # Handle piece passing
            if action == 'pass_piece' and self.other_player.current_piece is None:
                passed_piece = self.current_player.current_piece
                if self.other_player.receive_piece(passed_piece):
                    self.current_player.current_piece = None
                    self.switch_turn()
                    self.cooperation_bonus += 50
            
            # Handle hard drop
            if action == 'hard_drop':
                self.place_current_piece()
        
        # Handle piece falling
        if current_time - self.last_fall_time > self.fall_time:
            self.fall_piece()
            self.last_fall_time = current_time
    
    def fall_piece(self):
        """Make the current piece fall one row"""
        if not self.current_player.current_piece:
            return
        
        test_piece = self.current_player.current_piece.copy()
        test_piece.move(0, 1)
        
        if self.board.is_valid_position(test_piece):
            self.current_player.current_piece.move(0, 1)
        else:
            self.place_current_piece()
    
    def place_current_piece(self):
        """Place the current piece on the board"""
        if not self.current_player.current_piece:
            return
        
        # Place the piece
        lines_cleared = self.board.place_piece(self.current_player.current_piece, self.current_player.id)
        
        # Calculate score
        base_score = 0
        if lines_cleared > 0:
            base_score = lines_cleared * 100 * lines_cleared  # Exponential scoring
            self.current_player.lines_contributed += lines_cleared
        
        # Add cooperation bonus
        if lines_cleared > 0 and self.cooperation_bonus > 0:
            base_score += self.cooperation_bonus
            self.cooperation_bonus = 0
        
        # Update scores
        self.current_player.add_score(base_score)
        self.shared_score += base_score
        self.current_player.piece_placed()
        
        # Check for game over
        if self.board.is_game_over():
            self.game_over = True
            return
        
        # Switch turns after placing a piece
        self.switch_turn()
    
    def draw_board(self):
        """Draw the game board"""
        # Draw board outline
        board_rect = pygame.Rect(BOARD_X - 2, BOARD_Y - 2, 
                                BOARD_WIDTH * CELL_SIZE + 4, 
                                BOARD_HEIGHT * CELL_SIZE + 4)
        pygame.draw.rect(self.screen, WHITE, board_rect, 2)
        
        # Draw grid
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                cell_rect = pygame.Rect(BOARD_X + x * CELL_SIZE, 
                                      BOARD_Y + y * CELL_SIZE, 
                                      CELL_SIZE, CELL_SIZE)
                
                # Draw cell
                pygame.draw.rect(self.screen, self.board.grid[y][x], cell_rect)
                pygame.draw.rect(self.screen, GRAY, cell_rect, 1)
    
    def draw_piece(self, piece, offset_x=0, offset_y=0):
        """Draw a tetris piece"""
        if not piece:
            return
        
        cells = piece.get_cells()
        for x, y in cells:
            if y >= 0:  # Only draw visible cells
                cell_rect = pygame.Rect(BOARD_X + (x + offset_x) * CELL_SIZE, 
                                      BOARD_Y + (y + offset_y) * CELL_SIZE, 
                                      CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, piece.color, cell_rect)
                pygame.draw.rect(self.screen, WHITE, cell_rect, 2)
    
    def draw_ghost_piece(self):
        """Draw ghost piece showing where current piece will land"""
        if not self.current_player.current_piece:
            return
        
        drop_y = self.board.get_drop_position(self.current_player.current_piece)
        ghost_piece = self.current_player.current_piece.copy()
        ghost_piece.y = drop_y
        
        # Draw ghost piece with transparency effect
        cells = ghost_piece.get_cells()
        for x, y in cells:
            if y >= 0:
                cell_rect = pygame.Rect(BOARD_X + x * CELL_SIZE, 
                                      BOARD_Y + y * CELL_SIZE, 
                                      CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, LIGHT_GRAY, cell_rect, 2)
    
    def draw_ui(self):
        """Draw user interface elements"""
        # Title
        title = self.font.render("Cooperative Tetris", True, WHITE)
        self.screen.blit(title, (SCORE_X, 10))
        
        # Shared score
        score_text = self.font.render(f"Shared Score: {self.shared_score}", True, WHITE)
        self.screen.blit(score_text, (SCORE_X, SCORE_Y))
        
        # Player scores
        p1_score = self.small_font.render(f"Player 1: {self.player1.score}", True, PLAYER_1_COLOR)
        self.screen.blit(p1_score, (SCORE_X, SCORE_Y + 40))
        
        p2_score = self.small_font.render(f"Player 2: {self.player2.score}", True, PLAYER_2_COLOR)
        self.screen.blit(p2_score, (SCORE_X, SCORE_Y + 60))
        
        # Current player indicator
        current_text = self.font.render(f"Current: Player {self.current_player.id}", 
                                      True, self.current_player.color)
        self.screen.blit(current_text, (PLAYER_INDICATOR_X, PLAYER_INDICATOR_Y))
        
        # Turn timer
        current_time = time.time() * 1000
        time_left = max(0, self.turn_duration - (current_time - self.turn_switch_timer)) / 1000
        timer_text = self.small_font.render(f"Time left: {time_left:.1f}s", True, WHITE)
        self.screen.blit(timer_text, (PLAYER_INDICATOR_X, PLAYER_INDICATOR_Y + 30))
        
        # Next pieces
        next1_text = self.small_font.render("Player 1 Next:", True, PLAYER_1_COLOR)
        self.screen.blit(next1_text, (NEXT_PIECE_X, NEXT_PIECE_Y))
        
        next2_text = self.small_font.render("Player 2 Next:", True, PLAYER_2_COLOR)
        self.screen.blit(next2_text, (NEXT_PIECE_X, NEXT_PIECE_Y + 100))
        
        # Cooperation bonus
        if self.cooperation_bonus > 0:
            bonus_text = self.small_font.render(f"Cooperation Bonus: +{self.cooperation_bonus}", 
                                              True, GREEN)
            self.screen.blit(bonus_text, (SCORE_X, SCORE_Y + 100))
        
        # Controls
        controls_y = 400
        controls = [
            "Player 1: WASD + Q(drop) + E(pass)",
            "Player 2: IJKL + U(drop) + O(pass)",
            "SPACE: Pause | TAB: Switch turn | R: Restart"
        ]
        
        for i, control in enumerate(controls):
            control_text = self.small_font.render(control, True, WHITE)
            self.screen.blit(control_text, (10, controls_y + i * 20))
        
        # Game over screen
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.fill(BLACK)
            overlay.set_alpha(180)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font.render("GAME OVER", True, RED)
            final_score_text = self.font.render(f"Final Shared Score: {self.shared_score}", True, WHITE)
            restart_text = self.small_font.render("Press R to restart", True, WHITE)
            
            # Center the text
            self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50))
            self.screen.blit(final_score_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2))
            self.screen.blit(restart_text, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 + 50))
        
        # Pause screen
        if self.paused and not self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.fill(BLACK)
            overlay.set_alpha(180)
            self.screen.blit(overlay, (0, 0))
            
            pause_text = self.font.render("PAUSED", True, WHITE)
            continue_text = self.small_font.render("Press SPACE to continue", True, WHITE)
            
            self.screen.blit(pause_text, (SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 - 20))
            self.screen.blit(continue_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 20))
    
    def restart_game(self):
        """Restart the game"""
        self.board = GameBoard()
        self.player1 = Player(1, PLAYER_1_COLOR)
        self.player2 = Player(2, PLAYER_2_COLOR)
        self.current_player = self.player1
        self.other_player = self.player2
        
        self.shared_score = 0
        self.cooperation_bonus = 0
        self.game_over = False
        self.paused = False
        
        self.player1.spawn_new_piece()
        self.player2.spawn_new_piece()
        self.switch_turn()
    
    def run(self):
        """Main game loop"""
        while self.running:
            # Handle events
            keys_pressed = self.handle_events()
            
            # Update game logic
            self.update_game_logic(keys_pressed)
            
            # Draw everything
            self.screen.fill(BLACK)
            self.draw_board()
            self.draw_ghost_piece()
            self.draw_piece(self.current_player.current_piece)
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
