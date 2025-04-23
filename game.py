import pygame
import sys
from game_logic import GameLogic
from game_graphics import GameGraphics
from menu import main_menu


def main():
    pygame.init()
    clock = pygame.time.Clock()
    FPS = 60

    # Screen dimensions
    SCREEN_WIDTH = 1250
    SCREEN_HEIGHT = 600

    # Initialize game components
    game_logic = GameLogic(SCREEN_WIDTH, SCREEN_HEIGHT)
    game_graphics = GameGraphics(SCREEN_WIDTH, SCREEN_HEIGHT)

    # Game loop
    run = True
    while run:
        clock.tick(FPS)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Get keyboard input
        keys = pygame.key.get_pressed()

        # Update game logic
        remaining_time = game_logic.update(keys)

        # Check for game completion
        if remaining_time == -1:
            # Game complete, return to main menu
            return main_menu()

        # Render the game
        game_graphics.render_game(game_logic, remaining_time)

    pygame.quit()


if __name__ == "__main__":
    main()