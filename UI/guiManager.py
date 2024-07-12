from typing import List
from pygame_gui.core.gui_type_hints import Coordinate, RectLike
import pygame
from UI.guiElement import GUIElement

class GUIManager():
    def __init__(self, *guiElements: GUIElement) -> None:
        self.elements = list(guiElements)
        
    def add_elements(self, *guiElements: GUIElement):
        self.elements.extend(list(guiElements))
        print(self.elements)
        
    def process_events(self, event: pygame.Event):
        for element in self.elements:
            element.handle_events(event)
    
    def update(self, dt: float):
        for element in self.elements:
            element.update(dt)
    
    def draw_ui(self, surf: pygame.Surface):
        for element in self.elements:
            element.draw(surf)