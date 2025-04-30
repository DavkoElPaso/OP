import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.initial_y = y
        self.vel = 10
        self.vel_y = 0
        self.isJump = False
        self.moving_right = False
        self.moving_left = False
        self.frame = 0
        self.invul_time = 0
        self.gravity = 0.8  # Snížená gravitace pro vyšší skoky
        self.on_ground = False
        self.jump_force = -18  # Zvýšená síla skoku

        # obrázky
        self.walkRight = [pygame.image.load("imgs/chuz1.png"), pygame.image.load("imgs/chuz2.png")]
        self.walkLeft = [pygame.image.load("imgs/chuz4.png"), pygame.image.load("imgs/chuz3.png")]
        self.char = pygame.image.load("imgs/stat.png")

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.char.get_width(), self.char.get_height())

    def handle_collision(self, obstacles):
        player_rect = self.get_rect()
        was_on_ground = self.on_ground
        self.on_ground = False

        # gravitace, pokud je ve vzduchu
        if not self.on_ground:
            self.vel_y += self.gravity
            self.y += self.vel_y

        # Seřadíme překážky podle vzdálenosti od hráče, aby detekce kolizí byla přesnější
        sorted_obstacles = sorted(obstacles,
                              key=lambda obs: (obs.x - self.x) ** 2 + (obs.y - self.y) ** 2)

        for obs in sorted_obstacles:
            obs_rect = pygame.Rect(obs.x, obs.y, obs.obs.get_width(), obs.obs.get_height())

            if player_rect.colliderect(obs_rect):
                # Nejprve vertikální kolize
                if self.vel_y > 0:  # Pohyb dolů
                    if player_rect.bottom > obs_rect.top and player_rect.top < obs_rect.top:
                        self.y = obs_rect.top - player_rect.height
                        self.vel_y = 0
                        self.on_ground = True
                        self.isJump = False
                elif self.vel_y < 0:  # Pohyb nahoru
                    if player_rect.top < obs_rect.bottom:
                        self.y = obs_rect.bottom
                        self.vel_y = 0

                # Horizontální kolize
                player_rect = self.get_rect()  # Aktualizace rectu po vertikálním posunu
                if player_rect.colliderect(obs_rect):
                    if self.vel_y >= 0:  # Kontrola pouze při pádu, ne při výskoku
                        if player_rect.right > obs_rect.left and player_rect.centerx < obs_rect.centerx:
                            self.x = obs_rect.left - player_rect.width
                        elif player_rect.left < obs_rect.right and player_rect.centerx > obs_rect.centerx:
                            self.x = obs_rect.right

        # Kolize se zemí
        if self.y > 400:
            self.y = 400
            self.vel_y = 0
            self.on_ground = True
            self.isJump = False

        # Zabrání cukání postavy při stání
        if self.on_ground and was_on_ground and abs(self.vel_y) < 1:
            self.vel_y = 0

    def move(self, keys):
        # Pohyb do stran
        if keys[pygame.K_d]:
            self.x += self.vel
            self.moving_right = True
            self.moving_left = False
        elif keys[pygame.K_a]:
            self.x -= self.vel
            self.moving_left = True
            self.moving_right = False
        else:
            self.moving_right = False
            self.moving_left = False

        # Skok
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_force
            self.isJump = True
            self.on_ground = False

    def draw(self, screen, scroll):
        draw_x = self.x + scroll
        if self.moving_right:
            screen.blit(self.walkRight[self.frame // 10], (draw_x, self.y))
            self.frame = (self.frame + 1) % 20
        elif self.moving_left:
            screen.blit(self.walkLeft[self.frame // 10], (draw_x, self.y))
            self.frame = (self.frame + 1) % 20
        else:
            screen.blit(self.char, (draw_x, self.y))
