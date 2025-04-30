import pygame

class Obs:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.obs = pygame.image.load("imgs/obs.png")

    def draw(self, screen, scroll):
        screen.blit(self.obs, (self.x + scroll, self.y))