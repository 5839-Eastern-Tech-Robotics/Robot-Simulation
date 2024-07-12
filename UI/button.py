import pygame
from pygame.sprite import _Group

class Button(pygame.sprite.Sprite):
    def __init__(self, app, rect: pygame.Rect, color: pygame.Color | str, rounding: int = 2):
        super().__init__(app.main_group, app.UI_group)
        self.rect = rect
        self.image = pygame.Surface(rect.size)