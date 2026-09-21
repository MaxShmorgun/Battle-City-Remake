import sys
import pygame
from map_loader import Map

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 525

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle City Remake")

game_map = Map("assets/levels/map.json")

clock = pygame.time.Clock()
FPS = 60

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        game_map.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()