import pygame
import sys

from robot import Robot
from settings import *
from UI import *

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        self.bg = pygame.image.load("./assets/emptyField.png").convert()
        
        self.main_group = pygame.sprite.Group()
        self.robot = Robot(self)
        
        self.clock = pygame.time.Clock()
        self.delta_time = 0.01
        
        ######################
        #      INIT GUI      #
        ######################
        self.gui_manager = GUIManager()
        Dropdown(self, (625, 5, 100, 30), ["Pure Pursit", "Ramsette", "PID"])
        

    def update(self):
        self.main_group.update()
        self.gui_manager.update(self.delta_time)
        pygame.display.set_caption(f'{self.clock.get_fps(): .1f}')
        self.delta_time = self.clock.tick(60) / 1000

    def draw(self):
        self.screen.fill('white')
        self.screen.blit(self.bg, (0, 0))
        self.main_group.draw(self.screen)
        self.robot.draw(self.screen)
        self.gui_manager.draw_ui(self.screen)
        pygame.display.flip()

    def check_events(self):
        event_queue = pygame.event.get()
        for e in event_queue:
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                self.robot.user_driving = not self.robot.user_driving
                
            self.gui_manager.process_events(e)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    app = App()
    app.run()
