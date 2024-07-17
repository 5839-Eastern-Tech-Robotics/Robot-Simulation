from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from main import App

class BaseMovement:
    def __init__(self, app: App, running: bool = True):
        self.app = app
        self.robot = app.robot
        self.running = running
        
    def pause(self):
        self.robot.activeMovement = None
        self.robot.user_driving = True
        self.running = False
        
    def resume(self):
        self.robot.activeMovement = self
        self.robot.user_driving = False
        self.running = True
        
    def update(self, dt: float) -> Tuple[float, float]:
        return 0, 0