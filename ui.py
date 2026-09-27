import pygame
import os

import pygame

class PlayerHealth():
    HEART_SIZE = 60
    LEFT_MARGIN = 10
    BOTTOM_MARGIN = 8
    HEART_GAP = 1

    def __init__(self, player):
        self.player = player
        texture_path = os.path.join(
            os.path.dirname(__file__), "assets", "images", "heart.jpg"
        )
        heart = pygame.image.load(texture_path).convert()
        heart.set_colorkey(heart.get_at((0, 0)))
        self.heart_image = pygame.transform.scale(
            heart, (self.HEART_SIZE, self.HEART_SIZE)
        )
        self.health = player.health

    def update(self):
        self.health = max(0, min(self.player.health, 3))

    def draw(self, surface):
        top = surface.get_height() - self.HEART_SIZE - self.BOTTOM_MARGIN
        for index in range(self.health):
            left = self.LEFT_MARGIN + index * (self.HEART_SIZE + self.HEART_GAP)
            surface.blit(self.heart_image, (left, top))


class BaseHealth:
    def __init__(self, position, tile_w, tile_h, health=5):
        self.center = (
            int(position[0] + tile_w / 2),
            int(position[1] + tile_h / 2),
        )
        self.font = pygame.font.Font(None, int(min(tile_w, tile_h) * 0.65))
        self.health = health
        self.image = self.font.render(str(health), True, (20, 20, 20))

    def update(self, health):
        if health != self.health:
            self.health = health
            self.image = self.font.render(str(health), True, (20, 20, 20))

    def draw(self, surface):
        text_rect = self.image.get_rect(center=self.center)
        surface.blit(self.image, text_rect)