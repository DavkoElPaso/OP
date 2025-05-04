import pygame
import sys
from game_logic import GameLogic
from game_graphics import GameGraphics
from menu import main_menu


def main():
    # Inicializace Pygame
    pygame.init()
    clock = pygame.time.Clock()
    FPS = 60

    # Rozměry obrazovky
    SCREEN_WIDTH = 1250
    SCREEN_HEIGHT = 600

    # Inicializace herních komponent
    game_logic = GameLogic(SCREEN_WIDTH, SCREEN_HEIGHT)
    game_graphics = GameGraphics(SCREEN_WIDTH, SCREEN_HEIGHT)

    # Herní smyčka
    run = True
    while run:
        clock.tick(FPS)

        # Zpracování událostí
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Získání vstupu z klávesnice
        keys = pygame.key.get_pressed()

        # Aktualizace herní logiky
        remaining_time = game_logic.update(keys)

        # Kontrola dokončení hry
        if remaining_time == -1:
            # Hra dokončena, návrat do hlavního menu
            return main_menu()

        # Vykreslení hry
        game_graphics.render_game(game_logic, remaining_time)

    pygame.quit()


