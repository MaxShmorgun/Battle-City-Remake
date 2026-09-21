import json
import os
import pygame

COLORS = {
    "1": (139, 69, 19),
    "0": (0, 0, 0),
    "E": (255, 0, 0),
    "B": (100, 100, 100),
    "P": (0, 255, 0),
    "F": (255, 215, 0)
}

class Map:
    def __init__(self, file_path):
        self.file_path = file_path
        self.grid = self.load_map()

    def load_map(self):
        if not os.path.exists(self.file_path):
            return []
        
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("map_data", [])

    def draw(self, surface):
        if not self.grid:
            return

        screen_w, screen_h = surface.get_size()
        cols = len(self.grid[0])
        rows = len(self.grid)

        tile_w = screen_w / cols
        tile_h = screen_h / rows

        for row_index, row in enumerate(self.grid):
            for col_index, tile in enumerate(row):
                color = COLORS.get(str(tile), (0, 0, 0))
                rect = pygame.Rect(
                    col_index * tile_w, 
                    row_index * tile_h, 
                    tile_w + 1, 
                    tile_h + 1
                )
                pygame.draw.rect(surface, color, rect)