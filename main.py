from pygame import Rect, Surface, sprite
from pygame.time import Clock
import pygame
import pygame_gui
import sys

from robot import Robot
from settings import *


class App:
    def __init__(self):
        pygame.init()
        self.screen: Surface = pygame.display.set_mode(RES)
        self.bg: Surface = pygame.image.load("./assets/emptyField.png").convert()

        self.main_group: sprite.Group = sprite.Group()
        self.robot: Robot = Robot(self)

        self.clock: Clock = Clock()
        self.delta_time: float = 0.01

        ######################
        #      INIT GUI      #
        ######################
        self.ui_manager = pygame_gui.UIManager(RES)
        self.ui_elements = {}
        self.ui_elements["reset_path"] = pygame_gui.elements.UIButton(
            Rect(625, 5, 100, 30),
            "Reset Path",
            self.ui_manager
        )

    def update(self) -> None:
        self.main_group.update()
        self.ui_manager.update(self.delta_time)
        pygame.display.set_caption(f'{self.clock.get_fps(): .1f}')
        self.delta_time = self.clock.tick(60) / 1000

    def draw(self) -> None:
        self.screen.fill('white')
        self.screen.blit(self.bg, (0, 0))
        self.main_group.draw(self.screen)
        self.robot.draw(self.screen)
        self.ui_manager.draw_ui(self.screen)
        pygame.display.flip()

    def check_events(self) -> None:
        event_queue = pygame.event.get()
        for e in event_queue:
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                self.robot.user_driving = not self.robot.user_driving
                
            if e.type == pygame_gui.UI_BUTTON_PRESSED and e.ui_element == self.ui_elements['reset_path']:
                self.robot.clear_positions()

            self.ui_manager.process_events(e)

    def run(self) -> None:
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    app = App()
    app.run()
