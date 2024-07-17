from __future__ import annotations
from typing import Tuple, List, Sequence, overload
import math

from settings import DEG_TO_RAD

class Pose:
    def __init__(self, x: int | float = 0, y: int | float = 0, theta: int | float = 0) -> None:
        self.x = x
        self.y = y
        self.theta = theta
     
    def __repr__(self) -> str:
        return f'Pose({self.x}, {self.y}, {self.theta})'
    def __str__(self) -> str:
        return f'(x: {self.x}, y: {self.y}, theta: {self.theta})'
    
    def __eq__(self, other: Pose) -> bool:
        assert(isinstance(other, Pose))
        return self.x == other.x and self.y == other.y and self.theta == other.theta
    
    def __add__(self, other: Pose) -> Pose:
        assert(isinstance(other, Pose))
        return Pose(self.x + other.x, self.y + other.y, self.theta + other.theta)
    def __iadd__(self, other: Pose) -> Pose:
        assert(isinstance(other, Pose))
        self.x += other.x
        self.y += other.y
        self.theta += other.theta
        return self
    
    def __sub__(self, other: Pose) -> Pose:
        assert(isinstance(other, Pose))
        return Pose(self.x - other.x, self.y - other.y, self.theta - other.theta)
    def __isub__(self, other: Pose) -> Pose:
        assert(isinstance(other, Pose))
        self.x -= other.x
        self.y -= other.y
        self.theta -= other.theta
        return self
    
    @overload
    def __mul__(self, other: Pose) -> int | float: ...
    @overload
    def __mul__(self, other: int | float) -> Pose: ...
    def __mul__(self, other: Pose | int | float) -> Pose | int | float:
        assert(isinstance(other, (Pose, int, float)))
        if isinstance(other, Pose):
            return self.x * other.x + self.y * other.y
        return Pose(self.x * other, self.y * other, self.theta)
    def __rmul__(self, other: int | float) -> Pose:
        assert(isinstance(other, (int, float)))
        return Pose(self.x * other, self.y * other, self.theta)
    def __imul__(self, other: int | float) -> Pose:
        assert(isinstance(other, (int, float)))
        self.x *= other
        self.y *= other
        return self
    
    def __truediv__(self, other: int | float) -> Pose:
        assert(isinstance(other, (float, int)))
        return Pose(self.x / other, self.y / other, self.theta)
    def __itruediv__(self, other: int | float) -> Pose:
        assert(isinstance(other, (int, float)))
        self.x /= other
        self.y /= other
        return self
        
    def __complex__(self) -> complex:
        return complex(self.x, self.y)

    @overload
    def __getitem__(self, key: int) -> int | float: ...
    @overload
    def __getitem__(self, key: slice) -> List[int | float]: ...
    def __getitem__(self, key: int | slice) -> int | float | List[int | float]:
        assert(isinstance(key, (int, slice)))
        if isinstance(key, slice):
            values = []
            for i in range(3)[key]:
                if i == 0: values.append(self.x)
                elif i == 1: values.append(self.y)
                elif i == 2: values.append(self.theta)
                else: raise IndexError("out of range")
            return values
        
        if key == 0: return self.x
        elif key == 1: return self.y
        elif key == 2: return self.theta
        else: raise IndexError("out of range")
        
    def __copy__(self) -> Pose:
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result
        
    def lerp(self, other: Pose, t: float, lerpTheta: bool = False) -> Pose:
        return Pose(self.x + (other.x - self.x) * t, self.y + (other.y - self.y) * t, self.theta + ((other.theta - self.theta) * t) if lerpTheta else 0)
    
    def distance(self, other: Pose) -> float:
        return math.hypot(self.x - other.x, self.y - other.y)
    
    def angle(self, other: Pose) -> float:
        return math.atan2(other.y - self.y, other.x - self.x)
    
    def rotate(self, angle: int | float, radians: bool = True) -> Pose:
        if not radians:
            angle = angle * DEG_TO_RAD
            
        return Pose(self.x * math.cos(angle) - self.y * math.sin(angle), 
                    self.x * math.sin(angle) + self.y * math.cos(angle), 
                    self.theta)
    
    def scale(self, factor: int | float) -> Pose:
        return Pose(self.x * factor, self.y * factor, self.theta * factor)

    def getVector(self) -> Pose:
        return Pose(self.x, self.y)
    
    def project(self, onto: Pose) -> Pose:
        return (self * onto) / (onto * onto) * onto
    
    def magnitude(self) -> float:
        return math.sqrt(self.magnitude_squared())
    
    def magnitude_squared(self) -> float:
        return self * self
    
    
    