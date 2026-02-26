from typing import Tuple

class Brick:
    def __init__(
        self,
        x: float,
        y: float,
        width: int,
        height: int,
        hits_required: int,
        points: int
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.points = points

        self.hits_required = hits_required
        self.hits_remaining = hits_required  # tracks current health
        self._alive = True

    def hit(self) -> int:
        """
        Register a hit on this brick.
        Returns points awarded — 0 if brick survives, full points if destroyed.
        """
        if not self._alive:
            return 0

        self.hits_remaining -= 1

        if self.hits_remaining <= 0:
            self._alive = False
            return self.points

        return 0  # brick hit but not destroyed yet

    def is_alive(self) -> bool:
        """Return whether brick is still active."""
        return self._alive

    def reset(self) -> None:
        """Restore brick to original state."""
        self.hits_remaining = self.hits_required
        self._alive = True

    def get_bounds(self) -> Tuple[float, float, float, float]:
        """
        Return bounding box as (left, top, right, bottom).
        Used by CollisionEngine.
        """
        return (
            self.x,
            self.y,
            self.x + self.width,
            self.y + self.height
        )

    def __repr__(self) -> str:
        return (
            f"Brick(x={self.x}, y={self.y}, "
            f"hits_remaining={self.hits_remaining}, "
            f"alive={self._alive})"
        )