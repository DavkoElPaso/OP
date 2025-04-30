import pygame

class Pivo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.obs = pygame.image.load("imgs/pivo.png")

    def draw(self, screen, scroll):
        screen.blit(self.obs, (self.x + scroll, self.y))