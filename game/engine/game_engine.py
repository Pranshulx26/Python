import pygame
from typing import List

from core.ball import Ball
from core.paddle import Paddle
from core.brick import Brick
from core.game_state import GameState
from core.collision import CollisionEngine
from managers.sound_manager import SoundManager
from ui.renderer import Renderer
from ui.input_handler import InputHandler

# engine/game_engine.py

import pygame
from typing import List

from core.ball import Ball
from core.paddle import Paddle
from core.brick import Brick
from core.game_state import GameState
from core.collision import CollisionEngine
from managers.sound_manager import SoundManager
from managers.score_manager import ScoreManager
from ui.renderer import Renderer
from ui.input_handler import InputHandler


class GameEngine:
    def __init__(
        self,
        ball: Ball,
        paddle: Paddle,
        bricks: List[Brick],
        game_state: GameState,
        collision: CollisionEngine,
        renderer: Renderer,
        input_handler: InputHandler,
        sound_manager: SoundManager,
        score_manager: ScoreManager

    ):
        self.ball = ball
        self.paddle = paddle
        self.bricks = bricks
        self.game_state = game_state
        self.collision = collision
        self.renderer = renderer
        self.input_handler = input_handler
        self.sound_manager = sound_manager

        self._running = False

    # -------------------------
    # Main Loop
    # -------------------------

    def run(self) -> None:
        """
        Main game loop — runs until player quits.
        Orchestrates update and render cycles.
        """
        self._running = True
        clock = pygame.time.Clock()

        while self._running:
            clock.tick(60) # limit to 60 FPS
            self._handle_events()

            if not self.game_state.is_paused \
            and not self.game_state.is_game_over \
            and not self.game_state.has_won:
                self._update()

            self._render()

    def _handle_events(self) -> None:
        """Process input events every frame."""
        events = self.input_handler.get_events()

        for event in events:
            if event.type == pygame.QUIT:
                self._running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self._handle_pause()
                if event.key == pygame.K_ESCAPE:
                    self._running = False

        # Continuous paddle movement
        direction = self.input_handler.get_paddle_direction()
        if direction:
            self.paddle.move(direction)

    def _update(self) -> None:
        """
        Core game logic — runs every frame when not paused.
        Orchestrates all updates in correct order.
        """
        self.ball.move()

        self._handle_wall_collisions()

        if self._handle_ball_lost():
            return  # skip rest of frame after life lost

        self._handle_paddle_collision()
        self._handle_brick_collisions()
        self._check_game_status()

    def _render(self) -> None:
        """Delegate all drawing to Renderer."""
        self.renderer.render(
            ball=self.ball,
            paddle=self.paddle,
            bricks=self.bricks,
            game_state=self.game_state
        )

    # -------------------------
    # Collision Handlers
    # -------------------------

    def _handle_wall_collisions(self) -> None:
        """Check and respond to ball hitting walls."""
        walls = self.collision.check_wall_collision(self.ball)

        if walls["left"] or walls["right"]:
            self.ball.bounce_horizontal()
            self.sound_manager.play("wall_hit")

        if walls["top"]:
            self.ball.bounce_vertical()
            self.sound_manager.play("wall_hit")

    def _handle_ball_lost(self) -> bool:
        """
        Check if ball fell below screen.
        Returns True if life was lost — caller skips rest of frame.
        """
        if not self.collision.check_ball_lost(self.ball):
            return False

        self.game_state.lose_life()
        self.sound_manager.play("life_lost")
        self.ball.reset()
        self.paddle.reset()
        return True

    def _handle_paddle_collision(self) -> None:
        """Check and respond to ball hitting paddle."""
        if self.collision.check_paddle_collision(self.ball, self.paddle):
            self.ball.bounce_vertical()
            self.sound_manager.play("paddle_hit")

    def _handle_brick_collisions(self) -> None:
        """
        Check ball against all bricks.
        Bounce once regardless of how many bricks hit.
        Process each hit brick individually.
        """
        hit_bricks = self.collision.check_brick_collision(
            self.ball,
            self.bricks
        )

        if not hit_bricks:
            return

        self.ball.bounce_vertical()  # bounce ONCE — not per brick

        for brick in hit_bricks:
            points = brick.hit()
            if points > 0:
                self.game_state.add_score(points)
                self.game_state.brick_destroyed()
                self.sound_manager.play("brick_destroyed")
            else:
                self.sound_manager.play("brick_hit")  # damaged not destroyed

    # -------------------------
    # Game Status
    # -------------------------

    def _check_game_status(self) -> None:
        """
        Read GameState flags and respond.
        Single place where win/lose consequences are handled.
        """
        if self.game_state.is_game_over:
            self._running = False

        if self.game_state.has_won:
            self._handle_level_complete()

    def _handle_level_complete(self) -> None:
        """Advance to next level and reset entities."""
        self.game_state.advance_level()
        self.ball.reset()
        self.paddle.reset()
        # LevelManager will reload bricks — coming soon

    def _handle_pause(self) -> None:
        """Toggle pause state."""
        self.game_state.toggle_pause()

    def __repr__(self) -> str:
        return f"GameEngine(running={self._running})"