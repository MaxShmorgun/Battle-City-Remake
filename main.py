import sys
import pygame
from map_loader import Map
from player import Player

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 525

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle City Remake")

game_map = Map("assets/levels/map.json")

cols = len(game_map.grid[0]) if game_map.grid else 13
rows = len(game_map.grid) if game_map.grid else 15
tile_w = SCREEN_WIDTH / cols
tile_h = SCREEN_HEIGHT / rows

player = Player(x=6 * tile_w, y=13 * tile_h, tile_w=tile_w, tile_h=tile_h, game_map=game_map)

clock = pygame.time.Clock()
FPS = 60

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update()

        screen.fill((0, 0, 0))
        game_map.draw(screen)
        player.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()