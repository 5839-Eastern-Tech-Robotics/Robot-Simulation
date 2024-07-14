from typing import List, Optional
from pygame_gui.core.gui_type_hints import Coordinate, RectLike
import pygame
from UI.guiElement import GUIElement

DROPDOWN_SELECTED_CHANGED = pygame.USEREVENT + 0

class Dropdown(GUIElement):
    def __init__(self, app, rect: RectLike, option_list: List[str], id: str = "Dropdown_", color = (99, 104, 107), highlight_color = (76, 80, 82), radius: int = 2, font: Optional[pygame.Font] = None, selected: int = 0):
        super().__init__(app, rect, id)
        self.option_list: List[str] = option_list
        self.selected: int = selected

        self._color = color
        self._highlight_color = highlight_color
        self._radius: int = radius
        self._font: pygame.Font = pygame.font.SysFont(None, 16) if font is None else font
        self._draw_menu: bool = False
        self._hovering_menu: bool = False
        self._hovered_option: int = -1

    def handle_events(self, event: pygame.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self._draw_menu = not self._draw_menu
            elif self._draw_menu and pygame.Rect(
                self.rect.x,
                self.rect.y + self.rect.height,
                self.rect.width,
                self.rect.height * len(self.option_list),
            ).collidepoint(pygame.mouse.get_pos()):
                self.selected = self._hovered_option
                self._draw_menu = False
                pygame.event.post(pygame.Event(DROPDOWN_SELECTED_CHANGED, {'ui_element': self}))
            else:
                self._draw_menu = False

    def draw(self, surf: pygame.Surface):
        if self.hidden: return
        pygame.draw.rect(
            surf,
            (
                self._highlight_color
                if self._hovering_menu or self._draw_menu
                else self._color
            ),
            self.rect,
            border_top_left_radius = self._radius,
            border_top_right_radius = self._radius,
            border_bottom_left_radius = -1 if self._draw_menu else self._radius,
            border_bottom_right_radius = -1 if self._draw_menu else self._radius,
        )
        msg = self._font.render(self.option_list[self.selected], True, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center = self.rect.center))

        if self._draw_menu:
            for i, text in enumerate(self.option_list):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(
                    surf,
                    self._highlight_color if i == self._hovered_option else self._color,
                    rect,
                    border_top_left_radius = -1 if self._draw_menu else self._radius,
                    border_top_right_radius = -1 if self._draw_menu else self._radius,
                    border_bottom_left_radius = self._radius,
                    border_bottom_right_radius = self._radius,
                )
                msg = self._font.render(text, True, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center = rect.center))
            outer_rect = (
                self.rect.x,
                self.rect.y,
                self.rect.width,
                self.rect.height * (len(self.option_list) + 1),
            )
            pygame.draw.rect(surf, (0, 0, 0), outer_rect, 2, self._radius)
        else:
            pygame.draw.rect(surf, (0, 0, 0), self.rect, 2, self._radius)

    def update(self, dt: float):
        mouse_pos = pygame.mouse.get_pos()
        self._hovering_menu = self.rect.collidepoint(mouse_pos)

        self._hovered_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(mouse_pos):
                self._hovered_option = i
