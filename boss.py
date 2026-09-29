import pygame
from enemy import Enemy


class Boss(Enemy):
    texture = None
    texture_file = "boss.png"

    def __init__(self, x, y, tile_w, tile_h, game_map):
        super().__init__(x, y, tile_w, tile_h, game_map)
        self.health = 7
        self.is_boss = True
        self.speed = 1

    def draw(self, surface):
        surface.blit(self.image, self.rect)

        bar_rect = pygame.Rect(self.rect.left, self.rect.top - 7, self.rect.width, 4)
        pygame.draw.rect(surface, (100, 0, 0), bar_rect)
        health_width = int(bar_rect.width * self.health / 7)
        if health_width > 0:
            pygame.draw.rect(
                surface,
                (0, 220, 0),
                (bar_rect.left, bar_rect.top, health_width, bar_rect.height),
            )