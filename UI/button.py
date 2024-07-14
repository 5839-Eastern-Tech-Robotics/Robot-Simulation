from typing import List, Optional
from pygame_gui.core.gui_type_hints import Coordinate, RectLike
import pygame
from UI.guiElement import GUIElement
from settings import HOLD_MIN_TIME, DOUBLE_CLICK_MAX_DELAY

BUTTON_ON_START_HOVER = pygame.USEREVENT + 1
BUTTON_ON_END_HOVER = pygame.USEREVENT + 2
BUTTON_ON_START_PRESS = pygame.USEREVENT + 3
BUTTON_ON_END_PRESS = pygame.USEREVENT + 4
BUTTON_ON_START_HOLD = pygame.USEREVENT + 5
BUTTON_ON_END_HOLD = pygame.USEREVENT + 6
BUTTON_ON_DOUBLE_CLICK = pygame.USEREVENT + 7

class Button(GUIElement):
    def __init__(self, app, rect: RectLike, text: str, id: str = "Button_", color = (99, 104, 107), highlight_color = (76, 80, 82), radius: int = 2, font: Optional[pygame.Font] = None):
        super().__init__(app, rect, id)

        self._color = color
        self._highlight_color = highlight_color
        self._radius: int = radius
        self._font: pygame.Font = pygame.font.SysFont(None, 16) if font is None else font
        self._text: str = text

        self.hovered: bool = False
        self.pressed: bool = False
        self.held: bool = False

        self._last_click_time: int = pygame.time.get_ticks()
        self._last_release_time: int = pygame.time.get_ticks()
        
    def set_text(self, text: str) -> None:
        self._text = text

    def handle_events(self, event: pygame.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
            self.on_click()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.pressed:
            self.on_release()

    def draw(self, surf: pygame.Surface) -> None:
        if self.hidden: return
        pygame.draw.rect(
            surf,
            self._highlight_color if self.hovered else self._color,
            self.rect,
            border_radius=self._radius,
        )
        msg = self._font.render(self._text, True, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center=self.rect.center))
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 2, self._radius)

    def update(self, dt: float) -> None:
        if not self.hovered and self.rect.collidepoint(pygame.mouse.get_pos()): self.on_enter_hover()
        elif self.hovered and not self.rect.collidepoint(pygame.mouse.get_pos()): self.on_exit_hover()
        if self._last_release_time < self._last_click_time and pygame.time.get_ticks() - self._last_click_time > HOLD_MIN_TIME and not self.held:
            self.held = True
            pygame.event.post(pygame.Event(BUTTON_ON_START_HOLD))
        
    def on_enter_hover(self):
        self.hovered = True
        pygame.event.post(pygame.Event(BUTTON_ON_START_HOVER, {'ui_element': self}))
        
    def on_exit_hover(self) -> None:
        self.hovered = False
        self.on_release()
        pygame.event.post(pygame.Event(BUTTON_ON_END_HOVER, {'ui_element': self}))
        
    def on_click(self) -> None:
        self.pressed = True
        self._last_click_time = pygame.time.get_ticks()
        if (self._last_click_time - self._last_release_time < DOUBLE_CLICK_MAX_DELAY):
            pygame.event.post(pygame.Event(BUTTON_ON_DOUBLE_CLICK, {'ui_element': self}))
        pygame.event.post(pygame.Event(BUTTON_ON_START_PRESS, {'ui_element': self}))
        
        
    def on_release(self) -> None:
        self.pressed = False
        held_prev = self.held
        self.held = False
        self._last_release_time = pygame.time.get_ticks()
        pygame.event.post(pygame.Event(BUTTON_ON_END_PRESS, {'ui_element': self}))
        if held_prev: pygame.event.post(pygame.Event(BUTTON_ON_END_HOLD, {'ui_element': self}))
        
