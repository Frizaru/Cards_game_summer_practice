import pygame

from config import (
    BACKGROUND_COLOR,
    FONT_NAME,
    IMAGE_SET_TITLES,
    MUTED_TEXT_COLOR,
    PANEL_BORDER_COLOR,
    PANEL_COLOR,
    TEXT_COLOR,
    WINDOW_WIDTH,
)
from menu import Button


class SetSelection:
    def __init__(self, image_sets):
        self.image_sets = image_sets
        self.title_font = pygame.font.SysFont(FONT_NAME, 64, bold=True)
        self.card_title_font = pygame.font.SysFont(FONT_NAME, 30, bold=True)
        self.hint_font = pygame.font.SysFont(FONT_NAME, 24)
        self.button_font = pygame.font.SysFont(FONT_NAME, 28, bold=True)
        self.back_button = Button((90, 950, 250, 58), "Главное меню", self.button_font)
        self.tiles = self._create_tiles()

    def _create_tiles(self):
        tiles = []
        tile_width = 420
        tile_height = 280
        gap_x = 54
        gap_y = 50
        start_x = (WINDOW_WIDTH - tile_width * 3 - gap_x * 2) // 2
        start_y = 265

        for index, set_key in enumerate(self.image_sets):
            row = index // 3
            col = index % 3
            rect = pygame.Rect(
                start_x + col * (tile_width + gap_x),
                start_y + row * (tile_height + gap_y),
                tile_width,
                tile_height,
            )
            tiles.append((set_key, rect))
        return tiles

    def handle_event(self, event):
        if self.back_button.was_clicked(event):
            return "menu", None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for set_key, rect in self.tiles:
                if rect.collidepoint(event.pos):
                    return "start", set_key
        return None, None

    def draw(self, surface):
        surface.fill(BACKGROUND_COLOR)

        title = self.title_font.render("Выберите набор", True, TEXT_COLOR)
        surface.blit(title, title.get_rect(center=(WINDOW_WIDTH // 2, 105)))

        hint = self.hint_font.render("Кликните по любому окошку, чтобы начать партию", True, MUTED_TEXT_COLOR)
        surface.blit(hint, hint.get_rect(center=(WINDOW_WIDTH // 2, 168)))

        for set_key, rect in self.tiles:
            self._draw_tile(surface, set_key, rect)

        self.back_button.draw(surface)

    def _draw_tile(self, surface, set_key, rect):
        pygame.draw.rect(surface, PANEL_COLOR, rect, border_radius=28)
        pygame.draw.rect(surface, PANEL_BORDER_COLOR, rect, width=2, border_radius=28)

        title = IMAGE_SET_TITLES.get(set_key, set_key.title())
        title_surface = self.card_title_font.render(title, True, TEXT_COLOR)
        surface.blit(title_surface, title_surface.get_rect(center=(rect.centerx, rect.y + 48)))

        preview = self.image_sets[set_key][0]
        preview_rect = preview.get_rect(center=(rect.centerx, rect.centery + 34))
        pygame.draw.rect(surface, (37, 27, 61), preview_rect.inflate(22, 22), border_radius=20)
        surface.blit(preview, preview_rect)
