# ui/renderer.py

import pygame
from typing import List

from core.ball import Ball
from core.paddle import Paddle
from core.brick import Brick
from core.game_state import GameState
from config import settings


class Renderer:
    """
    Responsible for ALL drawing.
    Reads object state — never modifies it.
    Single place where pygame.draw calls live.
    """

    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self._load_fonts()

    def _load_fonts(self) -> None:
        """Load fonts once at startup — not every frame."""
        self.font_large = pygame.font.SysFont("arial", 48)
        self.font_small = pygame.font.SysFont("arial", 24)

    def render(
        self,
        ball: Ball,
        paddle: Paddle,
        bricks: List[Brick],
        game_state: GameState
    ) -> None:
        """
        Master render method — called every frame.
        Decides which screen to draw based on game_state flags.
        """
        self._clear_screen()

        if game_state.is_game_over:
            self._draw_game_over(game_state)
        elif game_state.has_won:
            self._draw_win_screen(game_state)
        elif game_state.is_paused:
            self._draw_game(ball, paddle, bricks, game_state)
            self._draw_pause_overlay()
        else:
            self._draw_game(ball, paddle, bricks, game_state)

        pygame.display.flip()

    # -------------------------
    # Game Screen
    # -------------------------

    def _draw_game(
        self,
        ball: Ball,
        paddle: Paddle,
        bricks: List[Brick],
        game_state: GameState
    ) -> None:
        """Draw all active game elements."""
        self._draw_ball(ball)
        self._draw_paddle(paddle)
        self._draw_bricks(bricks)
        self._draw_hud(game_state)

    def _draw_ball(self, ball: Ball) -> None:
        pygame.draw.circle(
            self.surface,
            settings.BALL_COLOR,
            (int(ball.x), int(ball.y)),
            ball.radius
        )

    def _draw_paddle(self, paddle: Paddle) -> None:
        pygame.draw.rect(
            self.surface,
            settings.PADDLE_COLOR,
            (paddle.x, paddle.y, paddle.width, paddle.height)
        )

    def _draw_bricks(self, bricks: List[Brick]) -> None:
        for brick in bricks:
            if brick.is_alive():
                color = self._get_brick_color(brick)
                pygame.draw.rect(
                    self.surface,
                    color,
                    (brick.x, brick.y, brick.width, brick.height)
                )

    def _get_brick_color(self, brick: Brick) -> tuple:
        """
        Renderer decides color based on brick health.
        Brick stays pure — no color knowledge.
        """
        if brick.hits_remaining >= 3:
            return settings.BRICK_COLOR_STRONG
        elif brick.hits_remaining == 2:
            return settings.BRICK_COLOR_MEDIUM
        else:
            return settings.BRICK_COLOR_WEAK

    def _draw_hud(self, game_state: GameState) -> None:
        """Draw score and lives display."""
        score_text = self.font_small.render(
            f"Score: {game_state.score}",
            True,
            settings.HUD_COLOR
        )
        lives_text = self.font_small.render(
            f"Lives: {game_state.lives}",
            True,
            settings.HUD_COLOR
        )
        self.surface.blit(score_text, (10, 10))
        self.surface.blit(lives_text, (settings.SCREEN_WIDTH - 100, 10))

    # -------------------------
    # Overlay Screens
    # -------------------------

    def _draw_pause_overlay(self) -> None:
        """Semi-transparent pause screen over game."""
        pause_text = self.font_large.render(
            "PAUSED", True, settings.HUD_COLOR
        )
        self._draw_centered(pause_text)

    def _draw_game_over(self, game_state: GameState) -> None:
        game_over_text = self.font_large.render(
            "GAME OVER", True, (255, 0, 0)
        )
        score_text = self.font_small.render(
            f"Final Score: {game_state.score}",
            True,
            settings.HUD_COLOR
        )
        self._draw_centered(game_over_text, offset_y=-40)
        self._draw_centered(score_text, offset_y=20)

    def _draw_win_screen(self, game_state: GameState) -> None:
        win_text = self.font_large.render(
            "YOU WIN!", True, (0, 255, 0)
        )
        score_text = self.font_small.render(
            f"Final Score: {game_state.score}",
            True,
            settings.HUD_COLOR
        )
        self._draw_centered(win_text, offset_y=-40)
        self._draw_centered(score_text, offset_y=20)

    # -------------------------
    # Helpers
    # -------------------------

    def _clear_screen(self) -> None:
        self.surface.fill(settings.BACKGROUND_COLOR)

    def _draw_centered(
        self,
        surface: pygame.Surface,
        offset_y: int = 0
    ) -> None:
        """Draw any surface centered on screen."""
        x = (settings.SCREEN_WIDTH - surface.get_width()) // 2
        y = (settings.SCREEN_HEIGHT - surface.get_height()) // 2
        self.surface.blit(surface, (x, y + offset_y))

    def __repr__(self) -> str:
        return f"Renderer(surface={self.surface})"