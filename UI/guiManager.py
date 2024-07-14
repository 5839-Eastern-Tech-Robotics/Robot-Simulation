from __future__ import annotations
from typing import List, Iterator, overload
from collections import OrderedDict
from pygame_gui.core.gui_type_hints import Coordinate, RectLike
import pygame
from UI.guiElement import GUIElement

class GUIManager():
    def __init__(self, *guiElements: GUIElement) -> None:
        self.elements = OrderedDict((element.id, element) for element in guiElements)
        
    def add_elements(self, *guiElements: GUIElement) -> None:
        for element in guiElements:
            if element.id in self.elements.keys(): raise KeyError("element already exists")
            self.elements[element.id] = element
        
    def process_events(self, event: pygame.Event) -> None:
        for element in self.elements.values():
            element.handle_events(event)
    
    def update(self, dt: float) -> None:
        for element in self.elements.values():
            element.update(dt)
    
    def draw_ui(self, surf: pygame.Surface) -> None:
        for element in self.elements.values():
            element.draw(surf)
            
    def __getattr__(self, name: str) -> GUIElement:
        if name not in self.elements.keys(): raise AttributeError("id does not exist")
        return self.elements[name]
            
    def __len__(self) -> int:
        return len(self.elements)
    
    @overload
    def __getitem__(self, key: str | int) -> GUIElement: ...
    @overload
    def __getitem__(self, key: slice) -> List[GUIElement]: ...
    def __getitem__(self, key: str | int | slice) -> GUIElement | List[GUIElement]:
        if not isinstance(key, (int, slice, str)): raise TypeError(f"key must be one of str, int, slice got {type(key)=}")
        if isinstance(key, (int, slice)):
            return list(self.elements.values())[key]
        return self.elements[key]
    
    
    def __setitem__(self, key: str, value: GUIElement) -> None:
        if key != value.id: raise KeyError(f"key and element dont match got {key} as key and {value.id} as element id")
        if key in self.elements.keys(): raise KeyError("element already exists, you can't set this item")
        self.elements[key] = value
        
    def __delitem__(self, key: str | int) -> None:
        if isinstance(key, int): key = list(self.elements.keys())[key]     
        del self.elements[key]
        
    def __iter__(self) -> Iterator[GUIElement]:
        yield from self.elements.values()
        
    def __reversed__(self) -> GUIManager:
        return GUIManager(*reversed(self.elements.values()))
    
    def __contains__(self, item: GUIElement | str):
        return item in self.elements.keys() or item in self.elements.values()
    
    
    
    
        