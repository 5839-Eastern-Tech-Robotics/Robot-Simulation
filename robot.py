from __future__ import annotations
from pygame import Rect, Surface
import pygame
import math
import copy

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from main import App
    from movements.baseMovement import BaseMovement

from utils import Pose
from settings import *


class Robot(pygame.sprite.Sprite):
    def __init__(self, app: App) -> None:
        super().__init__(app.main_group)
        self.app: App = app
        self.activeMovement: Optional[BaseMovement] = None
        self.sprite: Surface = pygame.image.load("./assets/robot.png")
        self.sprite: Surface = pygame.transform.scale(self.sprite, (50, 50))
        self.image: Surface = self.sprite
        self.rect: Rect = self.sprite.get_rect()
        self.positions = [Pose(250, 250)]
        # self.noDrift = [Pose(250, 250)]

        self.leftWheelVel = self.rightWheelVel = 0
        self.wheelVel: list[float] = [self.leftWheelVel, self.rightWheelVel]
        self.user_driving: bool = True
        self.pose: Pose = Pose(250, 250)
        self.localMovement: Pose = Pose(0, 0)
        self.prevVel = Pose(0, 0)
        self.velocity = Pose(0, 0)

    def clear_positions(self):
        del self.positions[:-1]

    def _handle_input(self) -> None:
        self.prevVel = copy.copy(self.velocity)
        self.localMovement = Pose()

        key_state = pygame.key.get_pressed()

        if not self.user_driving: return

        if key_state[pygame.K_LEFT] or key_state[pygame.K_a]:
            self.localMovement.theta = (
                (ROBOT_MAX_WHEEL_VEL * PIXELS_PER_IN)
                / (ROBOT_TRACKWIDTH * math.pi)
                * RAD_TO_DEG
                * self.app.delta_time
            )
        if key_state[pygame.K_RIGHT] or key_state[pygame.K_d]:
            self.localMovement.theta = -(
                (ROBOT_MAX_WHEEL_VEL * PIXELS_PER_IN)
                / (ROBOT_TRACKWIDTH * math.pi)
                * RAD_TO_DEG
                * self.app.delta_time
            )

        if key_state[pygame.K_UP] or key_state[pygame.K_w]:
            self.localMovement = (
                Pose(0, -ROBOT_MAX_WHEEL_VEL * PIXELS_PER_IN, self.localMovement.theta)
                * self.app.delta_time
            )
        if key_state[pygame.K_DOWN] or key_state[pygame.K_s]:
            self.localMovement = (
                Pose(0, ROBOT_MAX_WHEEL_VEL * PIXELS_PER_IN, self.localMovement.theta)
                * self.app.delta_time
            )

        self.velocity = self.localMovement.rotate(-self.pose.theta, False)
        
        # self.noDrift.append(
        #     Pose(
        #         self.noDrift[-1].x + self.velocity.x,
        #         self.noDrift[-1].y + self.velocity.y,
        #         self.noDrift[-1].theta + self.velocity.theta
        #     )
        # )

    def _collision_test(self) -> None:
        self.pose.x += self.velocity.x
        self.pose.x = max(35, min(self.pose.x, 585))

        self.pose.y += self.velocity.y
        self.pose.y = max(35, min(self.pose.y, 585))

        self.pose.theta += self.velocity.theta
        
        if self.pose == self.positions[-1]: return
        self.positions.append(copy.copy(self.pose))

    def _handle_kinematics(self):
        if self.user_driving: return
        self.localMovement = Pose(
            0,
            (ROBOT_MAX_WHEEL_VEL * sum(self.wheelVel) / 2 * PIXELS_PER_IN),
            (
                ROBOT_MAX_WHEEL_VEL
                * (self.leftWheelVel - self.rightWheelVel)
                / (ROBOT_TRACKWIDTH * math.pi)
                * RAD_TO_DEG
                * PIXELS_PER_IN
            ),
        )

    def _handle_drift(self) -> None:
        forwardDir = Pose(math.sin(-self.pose.theta * DEG_TO_RAD), -math.cos(-self.pose.theta * DEG_TO_RAD))
        orthagonalDir = Pose(math.cos(-self.pose.theta * DEG_TO_RAD), math.sin(-self.pose.theta * DEG_TO_RAD))
        orthagonalMove = self.prevVel.project(orthagonalDir)
        self.velocity += orthagonalMove * ROBOT_DRIFT_FACTOR
        if self.localMovement.y == 0:
            self.velocity += self.prevVel.project(forwardDir) * ROBOT_DRIFT_FACTOR

    def _update_robot(self) -> None:
        self._handle_kinematics()
        self._handle_drift()
        self._collision_test()

    def _update_pygame_vars(self) -> None:
        self.image = pygame.transform.rotate(self.sprite, self.pose.theta)
        self.rect = self.image.get_rect(center=self.pose[:2])

    def update(self) -> None:
        super().update()
        self._handle_input()
        self._update_robot()
        self._update_pygame_vars()

    def draw(self, screen: Surface) -> None:
        prevPose = self.positions[0]
        for pose in self.positions[1:]:
            pygame.draw.line(screen, 'white', prevPose[:2], pose[:2], 3)
            prevPose = pose
        # prevPose = self.noDrift[0]
        # for pose in self.noDrift[1:]:
        #     pygame.draw.line(screen, 'red', prevPose[:2], pose[:2], 3)
        #     prevPose = pose
