import os

import pygame
from weapons import Weapon

class Player:
    def __init__(self, x, y, tile_w, tile_h, game_map):
        self.tile_w = tile_w
        self.tile_h = tile_h
        self.game_map = game_map
        
        self.rect = pygame.Rect(x, y, tile_w * 0.8, tile_h * 0.8)
        texture_path = os.path.join(
            os.path.dirname(__file__), "assets", "images", "player.jpg"
        )
        texture = pygame.image.load(texture_path).convert()
        self.image = pygame.transform.scale(texture, self.rect.size)
        self.speed = 4
        self.facing = "up"
        self.weapon = Weapon(tile_w, tile_h, game_map, (500, 525))
        self.health = 3

    def is_colliding(self, rect):
        grid = self.game_map.grid
        if not grid:
            return False

        start_col = max(0, int(rect.left // self.tile_w))
        end_col = min(len(grid[0]) - 1, int(rect.right // self.tile_w))
        start_row = max(0, int(rect.top // self.tile_h))
        end_row = min(len(grid) - 1, int(rect.bottom // self.tile_h))

        for r in range(start_row, end_row + 1):
            for c in range(start_col, end_col + 1):
                tile_type = grid[r][c]
                if tile_type in [1, "1", "B", "b"]:
                    tile_rect = pygame.Rect(c * self.tile_w, r * self.tile_h, self.tile_w, self.tile_h)
                    if rect.colliderect(tile_rect):
                        return True
        return False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        move_x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(
            keys[pygame.K_LEFT] or keys[pygame.K_a]
        )
        move_y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(
            keys[pygame.K_UP] or keys[pygame.K_w]
        )

        if move_x != 0:
            self.facing = "right" if move_x > 0 else "left"
            previous_x = self.rect.x
            self.rect.x += move_x * self.speed
            if self.is_colliding(self.rect):
                self.rect.x = previous_x

        if move_y != 0:
            self.facing = "down" if move_y > 0 else "up"
            previous_y = self.rect.y
            self.rect.y += move_y * self.speed
            if self.is_colliding(self.rect):
                self.rect.y = previous_y

    def update(self):
        self.handle_input()

    def fire(self):
        return self.weapon.fire(self.rect.center, self.facing)

    def draw(self, surface):
        surface.blit(self.image, self.rect)