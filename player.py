import pygame

class Player:
    def __init__(self, x, y, tile_w, tile_h, game_map):
        self.tile_w = tile_w
        self.tile_h = tile_h
        self.game_map = game_map
        
        self.rect = pygame.Rect(x, y, tile_w * 0.8, tile_h * 0.8)
        self.speed = 4

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
        move_x, move_y = 0, 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x = 1
            
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            move_y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            move_y = 1

        if move_x != 0:
            self.rect.x += move_x * self.speed
            if self.is_colliding(self.rect):
                if move_x > 0:
                    self.rect.right = (self.rect.right // self.tile_w) * self.tile_w
                else:
                    self.rect.left = (self.rect.left // self.tile_w + 1) * self.tile_w

        if move_y != 0:
            self.rect.y += move_y * self.speed
            if self.is_colliding(self.rect):
                if move_y > 0:
                    self.rect.bottom = (self.rect.bottom // self.tile_h) * self.tile_h
                else:
                    self.rect.top = (self.rect.top // self.tile_h + 1) * self.tile_h

    def update(self):
        self.handle_input()

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), self.rect)