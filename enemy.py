from collections import deque
import os
from random import randint
import pygame
from weapons import Weapon


class Enemy:
    texture = None
    DIRECTIONS = ("up", "right", "down", "left")
    MOVEMENT = {
        "up": (0, -1),
        "right": (1, 0),
        "down": (0, 1),
        "left": (-1, 0),
    }

    def __init__(self, x, y, tile_w, tile_h, game_map):
        self.tile_w = tile_w
        self.tile_h = tile_h
        self.game_map = game_map
        self.rect = pygame.Rect(x, y, tile_w * 0.8, tile_h * 0.8)
        self.rect.center = (int(x + tile_w / 2), int(y + tile_h / 2))
        if Enemy.texture is None:
            texture_path = os.path.join(
                os.path.dirname(__file__), "assets", "images", "enemy.jpg"
            )
            Enemy.texture = pygame.image.load(texture_path).convert()
        self.image = pygame.transform.scale(Enemy.texture, self.rect.size)
        self.speed = randint(1, 2)
        self.active = True
        self.health = 1
        self.is_boss = False
        self.facing = "down"
        grid = game_map.grid
        screen_size = (len(grid[0]) * tile_w, len(grid) * tile_h)
        self.weapon = Weapon(
            tile_w, tile_h, game_map, screen_size, cooldown=randint(1000, 2000), owner="enemy"
        )
        self.target = self.find_target()
        self.path = self.find_path(self.current_cell(), self.target)

    def current_cell(self):
        return (
            int(self.rect.centery // self.tile_h),
            int(self.rect.centerx // self.tile_w),
        )

    def find_target(self):
        for row_index, row in enumerate(self.game_map.grid):
            for col_index, tile in enumerate(row):
                if tile == "F":
                    return row_index, col_index
        return None

    def find_path(self, start, goal):
        if goal is None:
            return []

        grid = self.game_map.grid
        rows = len(grid)
        cols = len(grid[0]) if rows else 0
        queue = deque([start])
        previous = {start: None}

        while queue and goal not in previous:
            row, col = queue.popleft()
            for direction in self.DIRECTIONS:
                move_x, move_y = self.MOVEMENT[direction]
                next_cell = (row + move_y, col + move_x)
                next_row, next_col = next_cell
                if not (0 <= next_row < rows and 0 <= next_col < cols):
                    continue
                if grid[next_row][next_col] in (1, "1", "B", "b"):
                    continue
                if next_cell not in previous:
                    previous[next_cell] = (row, col)
                    queue.append(next_cell)

        if goal not in previous:
            return []

        path = []
        cell = goal
        while cell != start:
            path.append(cell)
            cell = previous[cell]
        path.reverse()
        return path

    def is_colliding(self, rect):
        grid = self.game_map.grid
        if not grid:
            return False

        if (
            rect.left < 0
            or rect.top < 0
            or rect.right > len(grid[0]) * self.tile_w
            or rect.bottom > len(grid) * self.tile_h
        ):
            return True

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

    def update(self):
        if self.target is None or not self.path:
            return

        target_row, target_col = self.path[0]
        target_x = int((target_col + 0.5) * self.tile_w)
        target_y = int((target_row + 0.5) * self.tile_h)
        delta_x = target_x - self.rect.centerx
        delta_y = target_y - self.rect.centery

        if not delta_x and not delta_y:
            self.path.pop(0)
            if not self.path:
                return
            target_row, target_col = self.path[0]
            target_x = int((target_col + 0.5) * self.tile_w)
            target_y = int((target_row + 0.5) * self.tile_h)
            delta_x = target_x - self.rect.centerx
            delta_y = target_y - self.rect.centery

        if delta_x:
            move_x = min(self.speed, abs(delta_x)) * (1 if delta_x > 0 else -1)
            direction = "right" if move_x > 0 else "left"
            next_rect = self.rect.move(move_x, 0)
        else:
            move_y = min(self.speed, abs(delta_y)) * (1 if delta_y > 0 else -1)
            direction = "down" if move_y > 0 else "up"
            next_rect = self.rect.move(0, move_y)

        if not self.is_colliding(next_rect):
            self.rect = next_rect
            self.facing = direction

    def fire(self):
        return self.weapon.fire(self.rect.center, self.facing)

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.active = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)