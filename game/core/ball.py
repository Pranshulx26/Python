
from dataclasses import dataclass
from typing import Tuple

class Ball:
    def __init__(
        self,
        x: float,
        y: float,
        speed_x: float,
        speed_y: float,
        radius: int,
        color: Tuple[int, int, int]
    ):
        self.x = x 
        self.y = y 
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.radius = radius

        # store starting values for reset
        self._start_x = x 
        self._start_y = y 
        self._start_speed_x = speed_x
        self._start_speed_y = speed_y

    def move(self) -> None:
        """Move ball one step based on current speed."""
        self.x += self.speed_x
        self.y += self.speed_y

    def bounce_horizontal(self) -> None:
        """Reverse horizontal direction. Called on left/right wall collision."""
        self.speed_x *= -1


    def bounce_vertical(self):
        """Reverse vertical direction. Called on top wall, paddle, brick collision."""
        self.speed_y *= -1

    def reset(self):
        """Return ball to starting position and speed after life is lost."""
        self.x = self._start_x
        self.y = self._start_y
        self.speed_x = self._start_speed_x
        self.speed_y = self._start_speed_y

    def get_bounds(self) -> Tuple[float, float, float, float]:
        """
        Return bounding box as (left, top, right, bottom).
        Used by CollisionEngine - keeps collision logic decoupled from Ball internals.
        """
        
        return (
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius
        )
    
    def __repr__(self) -> str:
        return (
            f'Ball(x={self.x}, y={self.y})'
            f'speed_x={self.speed_x}, speed_y={self.speed_y}'
        )