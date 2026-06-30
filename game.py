import random

import pygame

from card import Card
from config import (
    BACKGROUND_COLOR,
    CARD_GAP,
    CARD_SIZE,
    FLIP_BACK_DELAY_MS,
    FONT_NAME,
    GRID_COLS,
    GRID_ROWS,
    GRID_TOP,
    IMAGE_SET_TITLES,
    MUTED_TEXT_COLOR,
    PANEL_COLOR,
    TEXT_COLOR,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from menu import Button


class Game:
    def __init__(self, set_key, card_images, card_back):
        self.set_key = set_key
        self.card_images = card_images
        self.card_back = card_back
        self.title_font = pygame.font.SysFont(FONT_NAME, 62, bold=True)
        self.info_font = pygame.font.SysFont(FONT_NAME, 34)
        self.button_font = pygame.font.SysFont(FONT_NAME, 30, bold=True)
        self.win_font = pygame.font.SysFont(FONT_NAME, 74, bold=True)
        self._create_buttons()
        self.start_new_game()

    def _create_buttons(self):
        button_y = WINDOW_HEIGHT - 92
        button_height = 62
        gap = 24
        total_width = 210 + 280 + 170 + gap * 2
        left = (WINDOW_WIDTH - total_width) // 2
        self.restart_button = Button((left, button_y, 210, button_height), "Заново", self.button_font)
        self.menu_button = Button((left + 210 + gap, button_y, 280, button_height), "Главное меню", self.button_font)
        self.exit_button = Button((left + 210 + gap + 280 + gap, button_y, 170, button_height), "Выход", self.button_font)

    def start_new_game(self):
        self.moves = 0
        self.cards = []
        self.open_cards = []
        self.wait_until = None
        self.won = False
        self._create_board()

    def _create_board(self):
        pairs = []
        for image_id, image in enumerate(self.card_images[:8]):
            pairs.append((image_id, image))
            pairs.append((image_id, image))
        random.shuffle(pairs)

        grid_width = GRID_COLS * CARD_SIZE + (GRID_COLS - 1) * CARD_GAP
        grid_height = GRID_ROWS * CARD_SIZE + (GRID_ROWS - 1) * CARD_GAP
        left = (WINDOW_WIDTH - grid_width) // 2
        top = GRID_TOP + max(0, (WINDOW_HEIGHT - GRID_TOP - 145 - grid_height) // 2)

        for index, (image_id, image) in enumerate(pairs):
            row = index // GRID_COLS
            col = index % GRID_COLS
            x = left + col * (CARD_SIZE + CARD_GAP)
            y = top + row * (CARD_SIZE + CARD_GAP)
            self.cards.append(Card(image_id, image, self.card_back, (x, y, CARD_SIZE, CARD_SIZE)))

    def handle_event(self, event):
        if self.restart_button.was_clicked(event):
            self.start_new_game()
            return None
        if self.menu_button.was_clicked(event):
            return "menu"
        if self.won and self.exit_button.was_clicked(event):
            return "quit"

        if self.won or self.wait_until is not None:
            return None

        for card in self.cards:
            if card.was_clicked(event) and card.can_open() and card not in self.open_cards:
                self._open_card(card)
                break
        return None

    def _open_card(self, card):
        card.open()
        self.open_cards.append(card)

        if len(self.open_cards) == 2:
            self.moves += 1
            first, second = self.open_cards
            if first.image_id == second.image_id:
                first.mark_matched()
                second.mark_matched()
                self.open_cards.clear()
                self.won = all(card.state == Card.MATCHED for card in self.cards)
            else:
                self.wait_until = pygame.time.get_ticks() + FLIP_BACK_DELAY_MS

    def update(self):
        if self.wait_until is None or pygame.time.get_ticks() < self.wait_until:
            return
        for card in self.open_cards:
            card.close()
        self.open_cards.clear()
        self.wait_until = None

    def draw(self, surface):
        surface.fill(BACKGROUND_COLOR)
        self._draw_header(surface)
        for card in self.cards:
            card.draw(surface)
        self.restart_button.draw(surface)
        self.menu_button.draw(surface)
        if self.won:
            self._draw_win_message(surface)

    def _draw_header(self, surface):
        title = self.title_font.render("Cards", True, TEXT_COLOR)
        surface.blit(title, (96, 48))

        set_title = IMAGE_SET_TITLES.get(self.set_key, self.set_key.title())
        set_label = self.info_font.render(f"Набор: {set_title}", True, MUTED_TEXT_COLOR)
        surface.blit(set_label, (96, 122))

        moves_label = self.info_font.render(f"Ходы: {self.moves}", True, TEXT_COLOR)
        surface.blit(moves_label, moves_label.get_rect(topright=(WINDOW_WIDTH - 96, 62)))

    def _draw_win_message(self, surface):
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((20, 24, 36, 145))
        surface.blit(overlay, (0, 0))

        panel = pygame.Rect(0, 0, 620, 300)
        panel.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40)
        pygame.draw.rect(surface, PANEL_COLOR, panel, border_radius=32)

        title = self.win_font.render("Победа!", True, TEXT_COLOR)
        surface.blit(title, title.get_rect(center=(panel.centerx, panel.y + 92)))

        text = self.info_font.render(f"Вы нашли все пары за {self.moves} ходов", True, MUTED_TEXT_COLOR)
        surface.blit(text, text.get_rect(center=(panel.centerx, panel.y + 168)))

        self.restart_button.draw(surface)
        self.menu_button.draw(surface)

