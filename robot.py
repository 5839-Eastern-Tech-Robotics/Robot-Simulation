import pygame
import math
import copy

from utils import Pose
from settings import *


class Robot(pygame.sprite.Sprite):
    def __init__(self, app):
        super().__init__(app.main_group)
        self.app = app
        self.sprite = pygame.image.load("./assets/robot.png")
        self.sprite = pygame.transform.scale(self.sprite, (50, 50))
        self.image = self.sprite
        self.rect = self.sprite.get_rect()
        
        self.wheelVel = vec2(0, 0)
        self.user_driving = True
        self.pose = Pose(250, 250)
        self.prevPose = Pose(250, 250)
        self.velocityPose = Pose(0, 0)
        self.accelerationPose = Pose(0, 0)

    def _handle_input(self):
        key_state = pygame.key.get_pressed()
        
        if not self.user_driving:
            return

        if key_state[pygame.K_LEFT] or key_state[pygame.K_a]:
            self.pose.theta += (
                (ROBOT_MAX_WHEEL_VEL * PIXELS_PER_IN)
                / (ROBOT_TRACKWIDTH * math.pi)
                * RAD_TO_DEG
                * self.app.delta_time
            )
        if key_state[pygame.K_RIGHT] or key_state[pygame.K_d]:
            self.pose.theta -= (
                (ROBOT_MAX_WHEEL_VEL * PIXELS_PER_IN)
                / (ROBOT_TRACKWIDTH * math.pi)
                * RAD_TO_DEG
                * self.app.delta_time
            )

        if key_state[pygame.K_UP] or key_state[pygame.K_w]:
            self.pose += (
                Pose(0, -ROBOT_MAX_WHEEL_VEL * PIXELS_PER_IN).rotate(
                    -self.pose.theta, False
                )
                * self.app.delta_time
            )
        if key_state[pygame.K_DOWN] or key_state[pygame.K_s]:
            self.pose += (
                Pose(0, ROBOT_MAX_WHEEL_VEL * PIXELS_PER_IN).rotate(
                    -self.pose.theta, False
                )
                * self.app.delta_time
            )
            
    def _update_robot(self):
        linVel = (self.wheelVel.x + self.wheelVel.y) / 2 * self.app.delta_time
        angVel = (self.wheelVel.x - self.wheelVel.y) / (math.pi * ROBOT_TRACKWIDTH) * self.app.delta_time
        self.pose.theta += angVel
        self.pose += Pose(linVel, 0).rotate(self.pose.theta)
                    

    def _update_pygame_vars(self):
        self.image = pygame.transform.rotate(self.sprite, self.pose.theta)
        self.rect = self.image.get_rect(center=self.pose[:2])

    def update(self):
        super().update()
        self._handle_input()
        self._update_robot()
        self._update_pygame_vars()
        
    def draw(self, screen):
        pass#pygame.draw.line(screen, 'yellow', self.pose[:2], (self.pose)[:2])
