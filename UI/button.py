from typing import List
from pygame_gui.core.gui_type_hints import Coordinate, RectLike
import pygame
from UI.guiElement import GUIElement

ON_ENTER_HOVER = pygame.USEREVENT + 0
ON_LEAVE_HOVER = pygame.USEREVENT + 0
ON_START_PRESS = pygame.USEREVENT + 0
ON_END_PRESS = pygame.USEREVENT + 0

class Button(GUIElement):
    def __init__(self, app, rect: RectLike, text: str, color = (99, 104, 107), highlight_color = (76, 80, 82), radius = 2, font = None):
        super().__init__(app, rect)
        
        self._color = color
        self._highlight_color = highlight_color
        self._radius = radius
        self._font = pygame.font.SysFont(None, 30) if font is None else font
        self._text = text
        
        self.pressed = False
        self.held = False
        self.hovered = False
        
        self.last_click_time = None
        self.last_release_time = None
        
    def handle_events(self, event: pygame.Event):
        pass
        
    def draw(self, surf: pygame.Surface):
        super().draw(surf)
    
    def update(self, dt: float):
        pass