import pygame
import math

class Background:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scroll = 0

        # Load images
        self.bg = pygame.image.load("imgs/pozadi.png").convert()
        self.bg_width = self.bg.get_width()
        self.grass = pygame.image.load("imgs/podlaha.png").convert()
        self.grass_width = self.grass.get_width()
        self.tiles = math.ceil(self.screen_width / self.bg_width) + 2  # Added one more tile for smooth scrolling

    def draw(self, screen):
        # Calculate the first tile position based on scroll
        first_tile = math.floor(abs(self.scroll) / self.bg_width)
        offset = self.scroll % self.bg_width

        # Draw background tiles
        for i in range(self.tiles):
            screen.blit(self.bg, ((i - 1) * self.bg_width + offset, 0))
            screen.blit(self.grass, ((i - 1) * self.grass_width + offset, 436))