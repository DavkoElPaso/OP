import pygame

class Enemy:
    def __init__(self, x, y):
        self.x = x  # World x-position
        self.y = y  # World y-position
        self.start_x = x
        self.move_range = 150  # Enemy moves from start_x to start_x + move_range
        self.direction = 1     # 1 = right, -1 = left
        self.speed = 3
        self.stepIndex = 0

        # Load images for animation
        self.left_enemy = [pygame.image.load("imgs/spachuz1.png"),
                        pygame.image.load("imgs/spachuz2.png")]
        self.right_enemy = [pygame.image.load("imgs/spachuz3.png"),
                         pygame.image.load("imgs/spachuz4.png")]

    def step(self):
        # Cycle between 0 and 1 for animation
        if self.stepIndex >= 1:
            self.stepIndex = 0

    def move(self):
        self.x += self.speed * self.direction
        if self.x <= self.start_x or self.x >= self.start_x + self.move_range:
            self.direction *= -1

    def draw(self, screen, scroll):
        self.step()
        draw_x = self.x + scroll
        if self.direction < 0:
            image = self.left_enemy[self.stepIndex]
        else:
            image = self.right_enemy[self.stepIndex]
        screen.blit(image, (draw_x, self.y))
        self.stepIndex += 1