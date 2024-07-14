from typing import List, Union, Sequence
from pygame_gui.core.gui_type_hints import Coordinate, RectLike
import pygame
from UI.guiElement import GUIElement

class Label(GUIElement):
    def __init__(self, app, rect: RectLike, txt: str, id: str = "Label_", color = (0, 0, 0), bgColor = (255, 255, 255), font = None):
        super().__init__(app, rect, id)
        self.text = txt
        self._color = color
        self._bgColor = bgColor
        self._font = font if font else pygame.font.SysFont(None, 16) 
        
    def draw(self, surf: pygame.Surface):
        if self.hidden: return
        text = self._font.render(self.text, True, self._color, self._bgColor, self.rect.width)
        surf.blit(text, self.rect, pygame.Rect((0, 0), self.rect.size))