from typing import Tuple

class Paddle:
    def __init__(
        self,
        x: float,
        y: float,
        width: int,
        height: int,
        speed: int,
        screen_width: int
    ):

        self.x = x 
        self.y = y 
        self.width = width
        self.height = height
        self.speed = speed 
        self.screen_width = screen_width

        # Store starting state for reset
        self._start_x = x 
        self._start_y = y 

    def move(self, direction: str) -> None:
        """
        Move paddle left or rigth.
        Boundary check is enforced automatically - paddle can never leave screen.
        """

        if direction == 'left':
            self.x -= self.speed
        elif direction == 'right':
            self.x += self.speed

        self._clamp_to_screen()

    def _clamp_to_screen(self) -> None:
        """
        Keep paddle within screen boundaries.
        Private method - caleed only by move().
        Outside world has no business calling this directly.
        """
        if self.x < 0:
            self.x = 0 
        if self.x + self.width > self.screen_width:
            self.x = self.screen_width - self.width 

    def reset(self) -> None:
        """Restore paddle to starting position."""
        self.x = self._start_x
        self.y = self._start_y

    def get_bounds(self) -> Tuple[float, float, float, float]:
        """
        Return bounding box as (left, top, right, bottom).
        CollisionEnginer uses this - never accesses internals directly.
        """

        return (
            self.x,
            self.y,
            self.x + self.width,
            self.y + self.height 
        )

    def __repr__(self) -> str:
        return f'Paddle(x={self.x}, y={self.y}, width={self.width})'