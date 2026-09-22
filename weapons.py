import pygame


DIRECTIONS = {
	"up": pygame.Vector2(0, -1),
	"down": pygame.Vector2(0, 1),
	"left": pygame.Vector2(-1, 0),
	"right": pygame.Vector2(1, 0),
}


class Bullet:
	def __init__(self, position, direction, tile_w, tile_h, game_map, screen_size):
		self.position = pygame.Vector2(position)
		self.direction = pygame.Vector2(direction)
		self.speed = 8
		self.radius = max(3, int(min(tile_w, tile_h) * 0.12))
		self.tile_w = tile_w
		self.tile_h = tile_h
		self.game_map = game_map
		self.screen_width, self.screen_height = screen_size
		self.active = True

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
			pygame.draw.circle(
				surface,
				(255, 255, 0),
				(int(self.position.x), int(self.position.y)),
				self.radius,
			)


class Weapon:
	def __init__(self, tile_w, tile_h, game_map, screen_size):
		self.tile_w = tile_w
		self.tile_h = tile_h
		self.game_map = game_map
		self.screen_size = screen_size

	def fire(self, position, facing):
		direction = DIRECTIONS.get(facing)
		if direction is None:
			raise ValueError(f"Unknown facing direction: {facing}")

		muzzle_offset = max(self.tile_w, self.tile_h) * 0.45
		spawn_position = pygame.Vector2(position) + direction * muzzle_offset
		return Bullet(
			spawn_position,
			direction,
			self.tile_w,
			self.tile_h,
			self.game_map,
			self.screen_size,
		)
