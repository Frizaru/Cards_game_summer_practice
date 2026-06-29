import pygame

from config import ASSETS_DIR, CARD_SIZE, IMAGE_SET_TITLES


SUPPORTED_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".gif")


def load_assets():
    card_back = _load_card_back()
    image_sets = {}
    for set_key in IMAGE_SET_TITLES:
        images = _load_set_images(set_key)
        image_sets[set_key] = images[:8]
    return image_sets, card_back


def _load_card_back():
    path = ASSETS_DIR / "card_back.png"
    if not path.exists():
        raise FileNotFoundError("Не найден файл assets/card_back.png")
    return _load_scaled_image(path)


def _load_set_images(set_key):
    folder = ASSETS_DIR / set_key
    if not folder.exists():
        raise FileNotFoundError(f"Не найдена папка набора: assets/{set_key}")

    paths = sorted(
        path for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )
    if len(paths) < 8:
        raise ValueError(f"В наборе assets/{set_key} должно быть минимум 8 картинок")
    return [_load_scaled_image(path) for path in paths[:8]]


def _load_scaled_image(path):
    image = pygame.image.load(str(path)).convert_alpha()
    return pygame.transform.smoothscale(image, (CARD_SIZE, CARD_SIZE))
