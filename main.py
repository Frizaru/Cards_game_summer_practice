import sys

import pygame

from assets import load_assets
from config import FPS, FULLSCREEN, WINDOW_HEIGHT, WINDOW_WIDTH
from game import Game
from menu import Menu
from set_selection import SetSelection


def main():
    pygame.init()
    pygame.display.set_caption("Cards")
    flags = pygame.FULLSCREEN if FULLSCREEN else 0
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags)
    clock = pygame.time.Clock()

    image_sets, card_back = load_assets()
    menu = Menu()
    set_selection = SetSelection(image_sets)
    game = None
    state = "menu"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif state == "menu":
                action, set_key = menu.handle_event(event)
                if action == "quit":
                    running = False
                elif action == "select":
                    state = "set_select"
            elif state == "set_select":
                action, set_key = set_selection.handle_event(event)
                if action == "menu":
                    state = "menu"
                elif action == "start":
                    game = Game(set_key, image_sets[set_key], card_back)
                    state = "game"
            elif state == "game" and game is not None:
                action = game.handle_event(event)
                if action == "quit":
                    running = False
                elif action == "menu":
                    state = "menu"

        if state == "game" and game is not None:
            game.update()
            game.draw(screen)
        elif state == "set_select":
            set_selection.draw(screen)
        else:
            menu.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
