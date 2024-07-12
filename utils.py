from typing import Tuple, List
import math

from settings import DEG_TO_RAD

class Pose:
    def __init__(self, x: int | float = 0, y: int | float = 0, theta: int | float = 0):
        self.x = x
        self.y = y
        self.theta = theta
     
    def __repr__(self):
        return f'Pose({self.x}, {self.y}, {self.theta})'
    def __str__(self):
        return f'(x: {self.x}, y: {self.y}, theta: {self.theta})'
    
    def __eq__(self, other):
        assert(isinstance(other, Pose))
        return self.x == other.x and self.y == other.y and self.theta == other.theta
    
    def __add__(self, other):
        assert(isinstance(other, Pose))
        return Pose(self.x + other.x, self.y + other.y, self.theta + other.theta)
    def __iadd__(self, other):
        assert(isinstance(other, Pose))
        self.x += other.x
        self.y += other.y
        self.theta += other.theta
        return self
    
    def __sub__(self, other):
        assert(isinstance(other, Pose))
        return Pose(self.x - other.x, self.y - other.y, self.theta - other.theta)
    def __isub__(self, other):
        assert(isinstance(other, Pose))
        self.x -= other.x
        self.y -= other.y
        self.theta -= other.theta
        return self
    
    def __mul__(self, other):
        assert(isinstance(other, (Pose, int, float)))
        if isinstance(other, Pose):
            return self.x * other.x + self.y * other.y
        return Pose(self.x * other, self.y * other, self.theta)
    def __rmul__(self, other):
        assert(isinstance(other, (int, float)))
        return Pose(self.x * other, self.y * other, self.theta)
    def __imul__(self, other):
        assert(isinstance(other, (int, float)))
        self.x *= other
        self.y *= other
        return self
    
    def __truediv__(self, other):
        assert(isinstance(other, (float, int)))
        return Pose(self.x / other, self.y / other, self.theta)
    def __itruediv__(self, other):
        assert(isinstance(other, (int, float)))
        self.x /= other
        self.y /= other
        return self
        
    def __complex__(self):
        return complex(self.x, self.y)

    def __getitem__(self, key):
        assert(isinstance(key, (int, slice)))
        if isinstance(key, slice):
            return [self[i] for i in range(3)[key]]
        
        if key == 0:
            return self.x
        if key == 1:
            return self.y
        if key == 2:
            return self.theta
        
    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result
        
    def lerp(self, other, t: float, lerpTheta: bool = False):
        return Pose(self.x + (other.x - self.x) * t, self.y + (other.y - self.y) * t, self.theta + ((other.theta - self.theta) * t) if lerpTheta else 0)
    
    def distance(self, other) -> float:
        return math.hypot(self.x - other.x, self.y - other.y)
    
    def angle(self, other) -> float:
        return math.atan2(other.y - self.y, other.x - self.x)
    
    def rotate(self, angle: int | float, radians: bool = True):
        if not radians:
            angle = angle * DEG_TO_RAD
            
        return Pose(self.x * math.cos(angle) - self.y * math.sin(angle), 
                    self.x * math.sin(angle) + self.y * math.cos(angle), 
                    self.theta)
    
    def scale(self, factor: int | float):
        return Pose(self.x * factor, self.y * factor, self.theta * factor)
