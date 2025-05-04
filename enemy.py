import pygame


class Enemy:
    def __init__(self, x, y):
        self.x = x  # x pozice ve světě
        self.y = y  # y pozice ve světě
        self.start_x = x  # počáteční x pozice (pro určení rozsahu pohybu)
        self.move_range = 150  # Nepřítel se pohybuje od start_x do start_x + move_range
        self.direction = 1  # Směr pohybu: 1 = doprava, -1 = doleva
        self.speed = 3  # Rychlost pohybu nepřítele
        self.animation_count = 0  # Počítadlo pro časování animace
        self.animation_speed = 10  # Určuje rychlost změny snímků animace (vyšší = pomalejší)

        # Načtení obrázků pro animaci nepřítele při pohybu doleva a doprava
        self.left_enemy = [pygame.image.load("imgs/spachuz1.png"),
                           pygame.image.load("imgs/spachuz2.png")]
        self.right_enemy = [pygame.image.load("imgs/spachuz3.png"),
                            pygame.image.load("imgs/spachuz4.png")]

    def move(self):
        # Posun nepřítele podle směru a rychlosti
        self.x += self.speed * self.direction

        # Pokud se dostane na kraj svého rozsahu, změní směr
        if self.x <= self.start_x or self.x >= self.start_x + self.move_range:
            self.direction *= -1  # Otočení směru

        # Aktualizace počítadla animace
        self.animation_count += 1
        if self.animation_count >= self.animation_speed * 2:  # Reset po dvou snímcích
            self.animation_count = 0

    def draw(self, screen, scroll):
        draw_x = self.x + scroll  # Vykreslovací pozice se započtením posunu kamery

        # Výběr snímku animace (0 nebo 1)
        frame = (self.animation_count // self.animation_speed) % 2

        # Výběr správného snímku podle směru pohybu
        if self.direction < 0:
            image = self.left_enemy[frame]
        else:
            image = self.right_enemy[frame]

        # Vykreslení nepřítele na obrazovku
        screen.blit(image, (draw_x, self.y))
