import pygame
import math
from player import Player
from enemy import Enemy
from obs import Obs
from pivo import Pivo
from coin import Coin


class GameLogic:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player = Player(170, 400)
        self.level = 1
        self.enemies = []
        self.obstacles = []
        self.pivo = None
        self.coin = None
        self.initial_enemies = []
        self.time_limit = 0
        self.start_time = pygame.time.get_ticks()
        self.level_scores = {1: 0, 2: 0, 3: 0}
        self.ENEMY_POINTS = 100
        self.COIN_POINTS = 200
        self.LEVEL_COMPLETE_POINTS = 500
        self.game_over = False

        self.load_level(self.level)

    def load_level(self, level):
        # čas na úroveň
        time_limits = {
            1: 24,
            2: 22,
            3: 20
        }

        # None, pokud není určeno v dané úrovni
        self.coin = None

        if level == 1:
            self.enemies = [Enemy(330, 400), Enemy(1120, 101), Enemy(1500, 101)]
            self.obstacles = [Obs(780, 370), Obs(1100, 200), Obs(1320, 200), Obs(1540, 200), Obs(1760, 200),
                              Obs(2150, 290)]
            self.pivo = Pivo(2220, 250)
            self.coin = Coin(1400, 400)
        elif level == 2:
            self.enemies = [Enemy(600, 261), Enemy(950, 141), Enemy(1750, 41), Enemy(2250, 41)]
            self.obstacles = [Obs(600, 360), Obs(950, 240), Obs(1250, 140), Obs(1750, 140), Obs(2250, 140),
                              Obs(2750, 140)]
            self.pivo = Pivo(2800, 100)
            self.coin = Coin(1700, 400)
        elif level == 3:
            self.enemies = [Enemy(920, 201), Enemy(1420, 150), Enemy(1920, 100), Enemy(2420, 50), Enemy(2920, 50),
                            Enemy(3420, 50)]
            self.obstacles = [Obs(600, 370), Obs(900, 300), Obs(1400, 250), Obs(1900, 200), Obs(2400, 150),
                              Obs(2900, 150), Obs(3400, 150)]
            self.pivo = Pivo(3540, 110)
            self.coin = Coin(1900, 400)
        else:
            self.game_over = True
            return False

        self.initial_enemies = [Enemy(enemy.x, enemy.y) for enemy in self.enemies]
        self.time_limit = time_limits[level]
        return True

    def reset_player(self):
        self.player.x = 170
        self.player.y = 400
        self.player.vel_y = 0
        self.player.invul_time = 60
        self.start_time = pygame.time.get_ticks()
        self.level_scores[self.level] = 0  # -body nepritel

    def update(self, keys):
        # zbývající čas
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        remaining_time = self.time_limit - elapsed_time

        if remaining_time <= 0:
            self.reset_player()
            return remaining_time

        # Aktualizuj hráče
        self.player.move(keys)
        self.player.handle_collision(self.obstacles)

        player_rect = self.player.get_rect()

        # jestli hráč sebral minci
        if self.coin:
            coin_rect = pygame.Rect(self.coin.x, self.coin.y,
                                    self.coin.obs.get_width(),
                                    self.coin.obs.get_height())
            if player_rect.colliderect(coin_rect):
                self.coin = None
                self.level_scores[self.level] += self.COIN_POINTS

        # pohyb nepřátel a kolize s hráčem
        enemies_to_remove = []
        for enemy in self.enemies:
            enemy.move()
            enemy_rect = pygame.Rect(enemy.x, enemy.y,
                                     enemy.left_enemy[0].get_width(),
                                     enemy.left_enemy[0].get_height())

            # jestli hráč skočil na nepřítele
            if self.player.vel_y > 0 and player_rect.bottom >= enemy_rect.top and player_rect.bottom <= enemy_rect.top + 20:
                if player_rect.right >= enemy_rect.left and player_rect.left <= enemy_rect.right:
                    enemies_to_remove.append(enemy)
                    self.player.vel_y = -10
                    self.level_scores[self.level] += self.ENEMY_POINTS
                    continue
            # jestli nepřítel zasáhl hráče
            elif self.player.invul_time == 0 and player_rect.colliderect(enemy_rect):
                self.reset_player()
                return remaining_time

        # Odstraň poražené nepřátele
        for enemy in enemies_to_remove:
            self.enemies.remove(enemy)

        # čas neporazitelnosti
        if self.player.invul_time > 0:
            self.player.invul_time -= 1

        # dokončení úrovně
        pivo_rect = pygame.Rect(self.pivo.x, self.pivo.y,
                                self.pivo.obs.get_width(),
                                self.pivo.obs.get_height())
        if player_rect.colliderect(pivo_rect):
            self.level_scores[self.level] += self.LEVEL_COMPLETE_POINTS
            self.level += 1
            if not self.load_level(self.level):
                self.save_scores()
                return -1  # dokončení hry

            self.player.x = 170
            self.player.y = 400
            self.player.vel_y = 0
            self.start_time = pygame.time.get_ticks()

        return remaining_time

    def save_scores(self):
        try:
            with open('highscores.txt', 'r') as f:
                high_scores = eval(f.read())
        except:
            high_scores = {1: 0, 2: 0, 3: 0}

        # Aktualizace skore
        for lvl in self.level_scores:
            if self.level_scores[lvl] > high_scores[lvl]:
                high_scores[lvl] = self.level_scores[lvl]

        with open('highscores.txt', 'w') as f:
            f.write(str(high_scores))
        with open('currentscores.txt', 'w') as f:
            f.write(str(self.level_scores))

    def get_scroll_position(self):
        # scroll podle pozice hráče
        return self.screen_width // 2 - self.player.x