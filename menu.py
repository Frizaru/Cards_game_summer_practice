import pygame

from config import (
    BACKGROUND_COLOR,
    DANGER_COLOR,
    FONT_NAME,
    MUTED_TEXT_COLOR,
    PANEL_COLOR,
    PANEL_BORDER_COLOR,
    PRIMARY_COLOR,
    TEXT_COLOR,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)


class Button:
    def __init__(self, rect, text, font, color=PRIMARY_COLOR):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.color = color

    def was_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=16)
        pygame.draw.rect(surface, PANEL_BORDER_COLOR, self.rect, width=2, border_radius=16)
        label = self.font.render(self.text, True, TEXT_COLOR)
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)


class Menu:
    def __init__(self):
        self.title_font = pygame.font.SysFont(FONT_NAME, 120, bold=True)
        self.subtitle_font = pygame.font.SysFont(FONT_NAME, 42)
        self.button_font = pygame.font.SysFont(FONT_NAME, 36, bold=True)
        self.small_font = pygame.font.SysFont(FONT_NAME, 28)
        self.buttons = self._create_buttons()

    def _create_buttons(self):
        button_width = 460
        button_height = 76
        start_y = 450
        gap = 26
        left = (WINDOW_WIDTH - button_width) // 2
        start_button = Button((left, start_y, button_width, button_height), "Начать партию", self.button_font)
        exit_y = start_y + button_height + gap
        exit_button = Button(
            (left, exit_y, button_width, button_height),
            "Выход",
            self.button_font,
            DANGER_COLOR,
        )
        return [("select", start_button), ("exit", exit_button)]

    def handle_event(self, event):
        for action, button in self.buttons:
            if button.was_clicked(event):
                if action == "exit":
                    return "quit", None
                return action, None
        return None, None

    def draw(self, surface):
        surface.fill(BACKGROUND_COLOR)
        panel = pygame.Rect(420, 110, WINDOW_WIDTH - 840, WINDOW_HEIGHT - 220)
        pygame.draw.rect(surface, PANEL_COLOR, panel, border_radius=36)
        pygame.draw.rect(surface, PANEL_BORDER_COLOR, panel, width=2, border_radius=36)

        title = self.title_font.render("Cards", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 235))
        surface.blit(title, title_rect)

        subtitle = self.subtitle_font.render("Игра на память", True, MUTED_TEXT_COLOR)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, 335))
        surface.blit(subtitle, subtitle_rect)

        for _, button in self.buttons:
            button.draw(surface)

        hint = self.small_font.render("Нажмите Начать партию, чтобы выбрать набор карточек", True, MUTED_TEXT_COLOR)
        hint_rect = hint.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 150))
        surface.blit(hint, hint_rect)
