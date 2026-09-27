import sys
import pygame


class Menu:

    def __init__(self, screen, width, height, background_path=None):
        self.screen = screen
        self.width = width
        self.height = height

        self.font_title = pygame.font.SysFont("arial", 42, bold=True)
        self.font_option = pygame.font.SysFont("arial", 28, bold=True)
        self.font_text = pygame.font.SysFont("arial", 20)

        self.options = ["Грати", "Правила гри", "Налаштування", "Вихід"]
        self.selected_index = 0
        self.sub_state = "main"

        self.volume = 0.5
        pygame.mixer.music.set_volume(self.volume)
        self.slider_rect = pygame.Rect(self.width // 2 - 100, self.height // 2, 200, 20)

        self.background = None
        if background_path:
            try:
                bg_img = pygame.image.load(background_path).convert()
                self.background = pygame.transform.scale(
                    bg_img, (self.width, self.height)
                )
            except Exception:
                self.background = None

        self.rules_text = [
            "ПРАВИЛА ГРИ:",
            "",
            "1. Керуйте персонажем (WASD / Стрілочки).",
            "2. Стріляйте по ворогах (Пробіл).",
            "3. Знищуйте хвилі ворогів.",
            "4. У вас є 3 життя (по 5 HP кожне).",
            "",
            "[ Натисніть ESC, ENTER або КЛІКНІТЬ, ]",
            "[ щоб повернутися ]",
        ]

    def play_menu_music(self):
        try:
            pygame.mixer.music.load("assets/sounds/background.mp3")
            pygame.mixer.music.play(-1)
        except Exception:
            pass

    def _get_option_rects(self):
        rects = []
        for i, option in enumerate(self.options):
            text_surface = self.font_option.render(option, True, (0, 0, 0))
            text_rect = text_surface.get_rect(
                center=(self.width // 2, self.height // 2 - 20 + i * 50)
            )
            rects.append(text_rect.inflate(40, 10))
        return rects

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.sub_state == "main":
            for i, rect in enumerate(self._get_option_rects()):
                if rect.collidepoint(mouse_pos):
                    self.selected_index = i

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.sub_state == "main":
                    for i, rect in enumerate(self._get_option_rects()):
                        if rect.collidepoint(mouse_pos):
                            if i == 0:
                                return "play"
                            elif i == 1:
                                self.sub_state = "rules"
                            elif i == 2:
                                self.sub_state = "settings"
                            elif i == 3:
                                pygame.quit()
                                sys.exit()

                elif self.sub_state == "rules":
                    self.sub_state = "main"

                elif self.sub_state == "settings":
                    if self.slider_rect.collidepoint(mouse_pos):
                        self.volume = (mouse_pos[0] - self.slider_rect.x) / self.slider_rect.width
                        pygame.mixer.music.set_volume(self.volume)
                    else:
                        self.sub_state = "main"

            if event.type == pygame.KEYDOWN:
                if self.sub_state == "main" and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if self.selected_index == 0:
                        return "play"
                    elif self.selected_index == 1:
                        self.sub_state = "rules"
                    elif self.selected_index == 2:
                        self.sub_state = "settings"
                    elif self.selected_index == 3:
                        pygame.quit()
                        sys.exit()
                elif self.sub_state in ("rules", "settings") and event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                    self.sub_state = "main"

        return "menu"

    def draw(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
        else:
            self.screen.fill((15, 15, 15))

        if self.sub_state == "main":
            self._draw_main_menu()
        elif self.sub_state == "rules":
            self._draw_rules()
        elif self.sub_state == "settings":
            self._draw_settings()

        pygame.display.flip()

    def _draw_main_menu(self):
        title_surface = self.font_title.render("BATTLE CITY REMAKE", True, (255, 215, 0))
        self.screen.blit(title_surface, (self.width // 2 - title_surface.get_width() // 2, self.height // 6))

        for i, option in enumerate(self.options):
            is_selected = i == self.selected_index
            color = (255, 255, 0) if is_selected else (220, 220, 220)
            text_surface = self.font_option.render(f"> {option} <" if is_selected else option, True, color)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 20 + i * 50))

            if is_selected:
                pygame.draw.rect(self.screen, (50, 50, 50), text_rect.inflate(20, 10), border_radius=8)
                pygame.draw.rect(self.screen, (255, 215, 0), text_rect.inflate(20, 10), width=2, border_radius=8)

            self.screen.blit(text_surface, text_rect)

    def _draw_rules(self):
        panel_rect = pygame.Rect(40, 40, self.width - 80, self.height - 80)
        pygame.draw.rect(self.screen, (20, 20, 20), panel_rect, border_radius=12)
        pygame.draw.rect(self.screen, (255, 215, 0), panel_rect, width=3, border_radius=12)

        start_y = 60
        for line in self.rules_text:
            color = (255, 215, 0) if "ПРАВИЛА" in line else ((150, 150, 150) if "[" in line else (255, 255, 255))
            font = self.font_option if "ПРАВИЛА" in line else self.font_text
            surf = font.render(line, True, color)
            self.screen.blit(surf, surf.get_rect(center=(self.width // 2, start_y)))
            start_y += 32

    def _draw_settings(self):
        panel_rect = pygame.Rect(40, 40, self.width - 80, self.height - 80)
        pygame.draw.rect(self.screen, (20, 20, 20), panel_rect, border_radius=12)
        pygame.draw.rect(self.screen, (255, 215, 0), panel_rect, width=3, border_radius=12)

        vol_text = self.font_option.render(f"Гучність: {int(self.volume * 100)}%", True, (255, 215, 0))
        self.screen.blit(vol_text, vol_text.get_rect(center=(self.width // 2, self.height // 2 - 40)))

        pygame.draw.rect(self.screen, (50, 50, 50), self.slider_rect, border_radius=6)
        fill_width = int(self.slider_rect.width * self.volume)
        if fill_width > 0:
            pygame.draw.rect(self.screen, (255, 215, 0), pygame.Rect(self.slider_rect.x, self.slider_rect.y, fill_width, self.slider_rect.height), border_radius=6)
        pygame.draw.rect(self.screen, (200, 200, 200), self.slider_rect, width=2, border_radius=6)