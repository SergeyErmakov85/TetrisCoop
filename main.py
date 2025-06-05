"""
Main entry point for the cooperative Tetris game
"""

from tetris_game import CooperativeTetris

def main():
    """Start the cooperative Tetris game"""
    try:
        game = CooperativeTetris()
        game.run()
    except Exception as e:
        print(f"Error starting game: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
