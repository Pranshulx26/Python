from typing import Dict, List, Tuple
from core.ball import Ball
from core.paddle import Paddle
from core.brick import Brick

class CollisionEngine:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

    def check_wall_collision(self, ball: Ball) -> Dict[str, bool]:
        """
        Check if ball has collided with any wall.
        Returns which walls were hit - caller decides consequences.
        """

        left, top, right, bottom = ball.get_bounds()

        return {
            'left': left <=0 ,
            'right': right >= self.screen_width,
            'top' : top <= 0,
            'bottom': bottom >= self.screen_height
        }

    def check_paddle_collision(
        self,
        ball: Ball,
        paddle: Paddle
    ) -> bool:
        """
        Check if ball is touching paddle.
        Returns True if collision detected.
        """

        return self._check_overlap(
            ball.get_bounds(),
            paddle.get_bounds()
        )

    def check_brick_collision(
        self,
        ball: Ball,
        bricks: List[Brick]
    ) -> List[Brick]:
        """
        Check ball against all alive bricks.
        Returns list of bricks that were hit this frame.
        Caller decides what to do - bounce, score, sound.
        """

        hit_bricks = []

        for brick in bricks:
            if not brick.is_alive():
                continue 
            if self._check_overlap(ball.get_bounds(), brick.get_bounds()):
                hit_bricks.append(brick)

        return hit_bricks
    

    def check_ball_lost(self, ball: Ball) -> bool:
        """
        Check if ball has fallen below the screen
        Separate from wall collision - different consequences entirely.
        """
        _, _, _, bottom = ball.get_bounds()
        return bottom >= self.screen_height

    def _check_overlap(
        self,
        bounds_a: Tuple[float, float, float, float],
        bounds_b: Tuple[float, float, float, float]
    ) -> bool:
        """
        Private helper - pure AABB overlap detection.
        Axis-Aligned Bounding Box check used for all rectangle collisions.
        """

        left_a, top_a, right_a, bottom_a = bounds_a
        left_b, top_b, right_b, bottom_b = bounds_b

        return (
            right_a >= left_b and 
            left_a <= right_b and 
            bottom_a >= top_b and 
            top_a <= bottom_b
        )

    def __repr__(self) -> str:
        return (
            f"CollisionEngine("
            f"screen={self.screen_width}x{self.screen_height}"
        )

