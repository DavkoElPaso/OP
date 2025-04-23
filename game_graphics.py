import pygame
import math


class GameGraphics:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Pivko SKS")

        # Load background images
        self.bg = pygame.image.load("imgs/pozadi.png").convert()
        self.bg_width = self.bg.get_width()
        self.grass = pygame.image.load("imgs/podlaha.png").convert()
        self.grass_width = self.grass.get_width()
        self.tiles = math.ceil(self.screen_width / self.bg_width) + 2

        # Initialize font for UI
        self.font = pygame.font.Font(None, 36)

    def draw_background(self, scroll):
        # Calculate the first tile position based on scroll
        first_tile = math.floor(abs(scroll) / self.bg_width)
        offset = scroll % self.bg_width

        # Draw background tiles
        for i in range(self.tiles):
            self.screen.blit(self.bg, ((i - 1) * self.bg_width + offset, 0))
            self.screen.blit(self.grass, ((i - 1) * self.grass_width + offset, 436))

    def draw_player(self, player, scroll):
        player.draw(self.screen, scroll)

    def draw_enemies(self, enemies, scroll):
        for enemy in enemies:
            enemy.draw(self.screen, scroll)

    def draw_obstacles(self, obstacles, scroll):
        for obstacle in obstacles:
            obstacle.draw(self.screen, scroll)

    def draw_pivo(self, pivo, scroll):
        pivo.draw(self.screen, scroll)

    def draw_coin(self, coin, scroll):
        if coin:
            coin.draw(self.screen, scroll)

    def draw_ui(self, remaining_time, level, score):
        # Draw timer
        timer_text = self.font.render(f"Time: {remaining_time}", True, (255, 255, 255))
        self.screen.blit(timer_text, (10, 10))

        # Draw score
        score_text = self.font.render(f"Level {level} Score: {score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 50))

    def clear_screen(self):
        self.screen.fill((0, 0, 0))

    def update_display(self):
        pygame.display.update()

    def render_game(self, game_logic, remaining_time):
        # Clear the screen
        self.clear_screen()

        # Get scroll position
        scroll = game_logic.get_scroll_position()

        # Draw background
        self.draw_background(scroll)

        # Draw game objects
        self.draw_obstacles(game_logic.obstacles, scroll)
        self.draw_coin(game_logic.coin, scroll)
        self.draw_pivo(game_logic.pivo, scroll)
        self.draw_player(game_logic.player, scroll)
        self.draw_enemies(game_logic.enemies, scroll)

        # Draw UI
        self.draw_ui(remaining_time, game_logic.level, game_logic.level_scores[game_logic.level])

        # Update display
        self.update_display()