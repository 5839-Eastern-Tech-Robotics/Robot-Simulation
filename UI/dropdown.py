from typing import List
from pygame_gui.core.gui_type_hints import Coordinate, RectLike
import pygame
from UI.guiElement import GUIElement

class Dropdown(GUIElement):
    def __init__(self, app, rect: RectLike, option_list: List[str], color = (99, 104, 107), highlight_color = (76, 80, 82), radius = 2, font = None, selected = 0):
        super().__init__(app, rect)
        self.option_list = option_list
        self.selected = selected
        
        self._color = color
        self._highlight_color = highlight_color
        self._radius = radius
        self._font = pygame.font.SysFont('arial', 16) if font is None else font
        self._draw_menu = False
        self._menu_active = False
        self._active_option = -1
        
    def handle_events(self, event: pygame.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._menu_active:
                self._draw_menu = not self._draw_menu
            elif self._draw_menu and self._active_option >= 0:
                self._selected = self._active_option
                self._draw_menu = False
                return self._active_option
        
    def draw(self, surf: pygame.Surface):
        super().draw(surf)
        pygame.draw.rect(surf, self._highlight_color if self._menu_active else self._color, self.rect)
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 2)
        msg = self._font.render(self.option_list[self.selected], 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center = self.rect.center))

        if self._draw_menu:
            for i, text in enumerate(self.option_list):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(surf, self._highlight_color if i == self._active_option else self._color, rect)
                msg = self._font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center = rect.center))
            outer_rect = (self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * len(self.option_list))
            pygame.draw.rect(surf, (0, 0, 0), outer_rect, 2)
    
    def update(self, dt: float):
        mpos = pygame.mouse.get_pos()
        self._menu_active = self.rect.collidepoint(mpos)
        
        self._active_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self._menu_active and self._active_option == -1:
            self._draw_menu = False            
        return -1