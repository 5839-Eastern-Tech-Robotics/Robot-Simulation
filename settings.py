import pygame
import math

vec2 = pygame.math.Vector2

# UNITS:
# length: inches
# time: second
# angle: radian

RES = WIDTH, HEIGHT = 1240, 620
CENTER = H_WIDTH, H_HEIGHT = WIDTH // 2, HEIGHT // 2

RAD_TO_DEG = 180 / math.pi
DEG_TO_RAD = math.pi / 180
#                     RPM         Wheel Diameter
ROBOT_MAX_WHEEL_VEL = 360 * (math.pi * 3.25) / 60
PIXELS_PER_IN = HEIGHT // 144
ROBOT_DRIFT_FACTOR = 0.8
ROBOT_TRACKWIDTH = 12
