import pygame

from config import CARD_BORDER_COLOR, MATCHED_BORDER_COLOR


class Card:
    CLOSED = "closed"
    OPEN = "open"
    MATCHED = "matched"

    def __init__(self, image_id, image, back_image, rect):
        self.image_id = image_id
        self.image = image
        self.back_image = back_image
        self.rect = pygame.Rect(rect)
        self.state = self.CLOSED

    def can_open(self):
        return self.state == self.CLOSED

    def open(self):
        if self.can_open():
            self.state = self.OPEN

    def close(self):
        if self.state == self.OPEN:
            self.state = self.CLOSED

    def mark_matched(self):
        self.state = self.MATCHED

    def was_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

    def draw(self, surface):
        image = self.image if self.state in (self.OPEN, self.MATCHED) else self.back_image
        surface.blit(image, self.rect)
        border_color = MATCHED_BORDER_COLOR if self.state == self.MATCHED else CARD_BORDER_COLOR
        pygame.draw.rect(surface, border_color, self.rect, width=3, border_radius=16)
