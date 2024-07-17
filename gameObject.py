import pygame
from pygame_gui.core.gui_type_hints import RectLike
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import App

class GameObject(pygame.sprite.Sprite):
    def __init__(self, app: App, rect: RectLike, surface: pygame.Surface, collidable: bool = True, moveable: bool = False, maxSpeedMod: float = 0) -> None:
        super().__init__(app.main_group)
        
        