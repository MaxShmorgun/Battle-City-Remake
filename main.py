import sys
import pygame
from boss import Boss
from enemy import Enemy
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

player_spawn = next(
    (
        (int(col_index * tile_w), int(row_index * tile_h))
        for row_index, row in enumerate(game_map.grid)
        for col_index, tile in enumerate(row)
        if tile == "P"
    ),
    (6 * tile_w, 13 * tile_h),
)
player = Player(x=player_spawn[0], y=player_spawn[1], tile_w=tile_w, tile_h=tile_h, game_map=game_map)
player.weapon.screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)

enemy_spawns = []
boss_spawn = None
for row_index, row in enumerate(game_map.grid):
    for col_index, tile in enumerate(row):
        if tile == "E":
            enemy_spawns.append((col_index * tile_w, row_index * tile_h))
            game_map.grid[row_index][col_index] = "0"
        elif tile == "B" and boss_spawn is None:
            boss_spawn = (col_index * tile_w, row_index * tile_h)
            game_map.grid[row_index][col_index] = "0"

def create_wave(wave_number):
    if wave_number == 10:
        return [("boss", boss_spawn)] if boss_spawn is not None else []
    if not enemy_spawns:
        return []

    enemy_count = len(enemy_spawns) + wave_number - 1
    return [
        ("enemy", enemy_spawns[index % len(enemy_spawns)])
        for index in range(enemy_count)
    ]

def victory():
    font = pygame.font.Font(None, 48)
    text = font.render(f"Victory!", True, (255, 255, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.fill((0, 0, 0))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(3000)

def lose():
    font = pygame.font.Font(None, 48)
    text = font.render(f"You lose!", True, (255, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.fill((0, 0, 0))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(3000)

def wave_completion_text(wave_number):
    font = pygame.font.Font(None, 48)
    text = font.render(f"Wave {wave_number} Complete!", True, (0, 255, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.fill((0, 0, 0))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(2000)

clock = pygame.time.Clock()
FPS = 60

def main():
    wave = 1
    base_health = 5
    spawn_queue = create_wave(wave)
    enemies = []
    bullets = []
    next_spawn_time = 0
    pygame.display.set_caption(f"Battle City Remake - Wave {wave}. Base HP: {base_health}.")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullet = player.fire()
                if bullet is not None:
                    bullets.append(bullet)

        player.update()
        current_time = pygame.time.get_ticks()
        if spawn_queue and current_time >= next_spawn_time:
            enemy_type, (x, y) = spawn_queue.pop(0)
            enemy_class = Boss if enemy_type == "boss" else Enemy
            enemies.append(enemy_class(x, y, tile_w, tile_h, game_map))
            next_spawn_time = current_time + 1000
        for enemy in enemies:
            enemy.update()
            if enemy.current_cell() == enemy.target:
                if enemy.is_boss:
                    lose()
                enemy.active = False
                pygame.display.set_caption(
                    f"Battle City Remake - Wave {wave}. Base HP: {base_health}."
                )
                if base_health <= 0:
                    lose()
                    running = False
                    break
                continue

            bullet = enemy.fire()
            if bullet is not None:
                bullets.append(bullet)
        if not running:
            break
        for bullet in bullets:
            bullet.update()
            if bullet.active:
                if bullet.owner == "player":
                    for enemy in enemies:
                        if enemy.active and bullet.collides_with(enemy.rect):
                            bullet.active = False
                            enemy.take_damage()
                            if enemy.is_boss and not enemy.active:
                                victory()
                                running = False
                            break
                elif bullet.owner == "enemy" and bullet.collides_with(player.rect):
                    bullet.active = False
                    player.health -= 1
                    if player.health <= 0:
                        lose()
                        running = False
                        break
        if not running:
            break
        bullets = [bullet for bullet in bullets if bullet.active]
        enemies[:] = [enemy for enemy in enemies if enemy.active]
        if wave < 10 and not enemies and not spawn_queue and enemy_spawns and player.health > 0 and base_health > 0:
            wave_completion_text(wave)
            player.rect.topleft = player_spawn
            player.facing = "up"
            wave += 1
            spawn_queue = create_wave(wave)
            pygame.display.set_caption(
                f"Battle City Remake - Wave {wave}. Base HP: {base_health}."
            )

        screen.fill((0, 0, 0))
        game_map.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        player.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()