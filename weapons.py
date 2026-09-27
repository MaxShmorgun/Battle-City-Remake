import os

import pygame


DIRECTIONS = {
	"up": pygame.Vector2(0, -1),
	"down": pygame.Vector2(0, 1),
	"left": pygame.Vector2(-1, 0),
	"right": pygame.Vector2(1, 0),
}


class Bullet:
	def __init__(self, position, direction, tile_w, tile_h, game_map, screen_size, owner="player"):
		self.position = pygame.Vector2(position)
		self.direction = pygame.Vector2(direction)
		self.owner = owner
		self.speed = 8
		self.radius = max(3, int(min(tile_w, tile_h) * 0.12))
		self.tile_w = tile_w
		self.tile_h = tile_h
		self.game_map = game_map
		self.screen_width, self.screen_height = screen_size
		self.active = True
		texture_path = os.path.join(
					os.path.dirname(__file__), "assets", "images", "bullet.jpg"
				)
		texture = pygame.image.load(texture_path).convert()
		self.image = pygame.transform.scale(texture, (self.radius * 4, self.radius * 4))
		angle = self.direction.angle_to(pygame.Vector2(0, -1))
		self.image = pygame.transform.rotate(self.image, angle)

	def is_colliding(self):
		grid = self.game_map.grid
		if not grid:
			return False

		bullet_rect = pygame.Rect(
			int(self.position.x - self.radius),
			int(self.position.y - self.radius),
			self.radius * 2,
			self.radius * 2,
		)
		start_col = max(0, int(bullet_rect.left // self.tile_w))
		end_col = min(len(grid[0]) - 1, int(bullet_rect.right // self.tile_w))
		start_row = max(0, int(bullet_rect.top // self.tile_h))
		end_row = min(len(grid) - 1, int(bullet_rect.bottom // self.tile_h))

		for row in range(start_row, end_row + 1):
			for col in range(start_col, end_col + 1):
				if grid[row][col] in [1, "1", "B", "b"]:
					tile_rect = pygame.Rect(
						col * self.tile_w,
						row * self.tile_h,
						self.tile_w,
						self.tile_h,
					)
					if bullet_rect.colliderect(tile_rect):
						return True
		return False

	def collides_with(self, rect):
		if not self.active:
			return False

		closest_x = max(rect.left, min(self.position.x, rect.right))
		closest_y = max(rect.top, min(self.position.y, rect.bottom))
		delta_x = self.position.x - closest_x
		delta_y = self.position.y - closest_y
		return delta_x * delta_x + delta_y * delta_y <= self.radius * self.radius

	def update(self):
		if not self.active:
			return

		self.position += self.direction * self.speed
		outside_screen = (
			self.position.x < 0
			or self.position.x > self.screen_width
			or self.position.y < 0
			or self.position.y > self.screen_height
		)
		if outside_screen or self.is_colliding():
			self.active = False

	def draw(self, surface):
		if self.active:
			image_rect = self.image.get_rect(center=self.position)
			surface.blit(self.image, image_rect)


class Weapon:
	def __init__(self, tile_w, tile_h, game_map, screen_size, cooldown=500, owner="player"):
		self.tile_w = tile_w
		self.tile_h = tile_h
		self.game_map = game_map
		self.screen_size = screen_size
		self.cooldown = cooldown
		self.owner = owner
		self.last_fire_time = None

	def fire(self, position, facing):
		direction = DIRECTIONS.get(facing)
		if direction is None:
			raise ValueError(f"Unknown facing direction: {facing}")

		current_time = pygame.time.get_ticks()
		if (
			self.last_fire_time is not None
			and current_time - self.last_fire_time < self.cooldown
		):
			return None

		muzzle_offset = max(self.tile_w, self.tile_h) * 0.45
		spawn_position = pygame.Vector2(position) + direction * muzzle_offset
		bullet = Bullet(
			spawn_position,
			direction,
			self.tile_w,
			self.tile_h,
			self.game_map,
			self.screen_size,
			self.owner,
		)
		self.last_fire_time = current_time
		return bullet
