from __future__ import annotations
from typing import List, TYPE_CHECKING
from pygame_gui.core.gui_type_hints import Coordinate, RectLike
from pygame import Rect, Surface
import pygame

if TYPE_CHECKING:
    from main import App


class GUIElement:
    ELEMENT_ID_NUM = 0
    def __init__(self, app, rect: RectLike, id: str = "Element_"):
        if not id.isidentifier(): raise ValueError(f"id must be valid python identifier, got: {id}")
        self.id: str = id + (str(GUIElement.ELEMENT_ID_NUM) if id[-1] == '_' else '')
        GUIElement.ELEMENT_ID_NUM += 1
        self.app: App = app
        self.rect: Rect = Rect(rect)
        self.hidden: bool = False
        self.app.gui_manager.add_elements(self)
        
    def hide(self) -> None:
        self.hidden = True
        
    def show(self) -> None:
        self.hidden = False
        
    def handle_events(self, event: pygame.Event) -> None:
        pass
        
    def draw(self, surf: pygame.Surface) -> None:
        if self.hidden: return
    
    def update(self, dt: float) -> None:
        pass

