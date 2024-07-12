from typing import List
from pygame_gui.core.gui_type_hints import Coordinate, RectLike
import pygame

class GUIElement:
    def __init__(self, app, rect: RectLike):
        self.app = app
        self.rect = pygame.Rect(rect)
        self.app.gui_manager.add_elements(self)
        self.hidden = False
        
    def handle_events(self, event: pygame.Event):
        pass
        
    def draw(self, surf: pygame.Surface):
        if self.hidden:
            return
    
    def update(self, dt: float):
        pass

