from __future__ import annotations
from pygame import Rect, Surface
import pygame
import math
import copy

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import App

from utils import Pose
from settings import *


class Robot(pygame.sprite.Sprite):
    def __init__(self, app: App) -> None:
        super().__init__(app.main_group)
        self.app: App = app
        self.sprite: Surface = pygame.image.load("./assets/robot.png")
        self.sprite: Surface = pygame.transform.scale(self.sprite, (50, 50))
        self.image: Surface = self.sprite
        self.rect: Rect = self.sprite.get_rect()
        
        self.wheelVel: vec2 = vec2(0, 0)
        self.user_driving: bool = True
        self.movement: Pose = Pose(0, 0)
        self.pose: Pose = Pose(250, 250)
        self.prevPose: Pose = Pose(250, 250)
        self.velocityPose: Pose = Pose(0, 0)
        self.accelerationPose: Pose = Pose(0, 0)

    def _handle_input(self) -> None:
        key_state = pygame.key.get_pressed()
        
        if not self.user_driving:
            return

        if key_state[pygame.K_LEFT] or key_state[pygame.K_a]:
            self.movement.theta = (
                (ROBOT_MAX_WHEEL_VEL * PIXELS_PER_IN)
                / (ROBOT_TRACKWIDTH * math.pi)
                * RAD_TO_DEG
                * self.app.delta_time
            )
        if key_state[pygame.K_RIGHT] or key_state[pygame.K_d]:
            self.movement.theta = -(
                (ROBOT_MAX_WHEEL_VEL * PIXELS_PER_IN)
                / (ROBOT_TRACKWIDTH * math.pi)
                * RAD_TO_DEG
                * self.app.delta_time
            )

        if key_state[pygame.K_UP] or key_state[pygame.K_w]:
            self.movement = (
                Pose(0, -ROBOT_MAX_WHEEL_VEL * PIXELS_PER_IN, self.movement.theta).rotate(
                    -self.pose.theta, False
                )
                * self.app.delta_time
            )
        if key_state[pygame.K_DOWN] or key_state[pygame.K_s]:
            self.movement = (
                Pose(0, ROBOT_MAX_WHEEL_VEL * PIXELS_PER_IN, self.movement.theta).rotate(
                    -self.pose.theta, False
                )
                * self.app.delta_time
            )
                        
    def _collision_test(self) -> None:
        self.pose.x += self.movement.x
        self.pose.x = max(35, min(self.pose.x, 585))
        
        self.pose.y += self.movement.y
        self.pose.y = max(35, min(self.pose.y, 585))
        
        self.pose.theta += self.movement.theta
        self.movement = Pose()
        
    def _update_robot(self) -> None:
        self._collision_test()
        
        # TODO: Impliment Drift
                    

    def _update_pygame_vars(self) -> None:
        self.image = pygame.transform.rotate(self.sprite, self.pose.theta)
        self.rect = self.image.get_rect(center=self.pose[:2])


    def update(self) -> None:
        super().update()
        self._handle_input()
        self._update_robot()
        self._update_pygame_vars()
        
    def draw(self, screen: Surface) -> None:
        pass#pygame.draw.line(screen, 'yellow', self.pose[:2], (self.pose)[:2])
