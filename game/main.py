# main.py

import pygame
from config import settings

from core.ball import Ball
from core.paddle import Paddle
from core.brick import Brick
from core.game_state import GameState
from core.collision import CollisionEngine

from engine.game_engine import GameEngine

from ui.screen import Screen
from ui.renderer import Renderer
from ui.input_handler import InputHandler

from managers.sound_manager import SoundManager
from managers.score_manager import ScoreManager


def create_ball() -> Ball:
    """Create ball with settings values."""
    return Ball(
        x=settings.SCREEN_WIDTH // 2,
        y=settings.SCREEN_HEIGHT // 2,
        speed_x=settings.BALL_SPEED_X,
        speed_y=settings.BALL_SPEED_Y,
        radius=settings.BALL_RADIUS,
        color=settings.BALL_COLOR  
    )


def create_paddle() -> Paddle:
    """Create paddle centered horizontally near bottom."""
    return Paddle(
        x=(settings.SCREEN_WIDTH - settings.PADDLE_WIDTH) // 2,
        y=settings.SCREEN_HEIGHT - settings.PADDLE_Y_OFFSET,
        width=settings.PADDLE_WIDTH,
        height=settings.PADDLE_HEIGHT,
        speed=settings.PADDLE_SPEED,
        screen_width=settings.SCREEN_WIDTH
    )


def create_bricks() -> list:
    """
    Generate brick grid from settings.
    Row position determines hit points and score value.
    """
    bricks = []

    for row in range(settings.BRICK_ROWS):
        for col in range(settings.BRICK_COLS):

            x = col * (settings.BRICK_WIDTH + settings.BRICK_PADDING)
            y = settings.BRICK_TOP_OFFSET + row * (
                settings.BRICK_HEIGHT + settings.BRICK_PADDING
            )

            # Top rows are tougher — more hits required
            hits_required = 3 if row < 2 else 2 if row < 4 else 1
            points = hits_required * 10

            bricks.append(Brick(
                x=x,
                y=y,
                width=settings.BRICK_WIDTH,
                height=settings.BRICK_HEIGHT,
                hits_required=hits_required,
                points=points
            ))

    return bricks


def create_game() -> GameEngine:
    """
    Composition root.
    Creates all objects, injects dependencies, returns wired engine.
    This is the ONLY place that knows about everyone simultaneously.
    """
    # Initialize pygame
    pygame.init()
    pygame.mixer.init()

    # Create screen first — surface needed by renderer
    screen = Screen()

    # Create all objects
    ball         = create_ball()
    paddle       = create_paddle()
    bricks       = create_bricks()
    game_state   = GameState(
                       initial_lives=settings.PLAYER_LIVES,
                       initial_level=1
                   )
    collision    = CollisionEngine(
                       screen_width=settings.SCREEN_WIDTH,
                       screen_height=settings.SCREEN_HEIGHT
                   )
    renderer     = Renderer(surface=screen.get_surface())
    input_handler = InputHandler()
    sound_manager = SoundManager()
    score_manager = ScoreManager()

    # Update game_state with initial brick count
    game_state.set_brick_count(len(bricks))

    # Wire everything into engine
    return GameEngine(
        ball=ball,
        paddle=paddle,
        bricks=bricks,
        game_state=game_state,
        collision=collision,
        renderer=renderer,
        input_handler=input_handler,
        sound_manager=sound_manager,
        score_manager=score_manager
    )


def main() -> None:
    """Entry point — create game and run."""
    game = create_game()
    game.run()
    pygame.quit()


if __name__ == "__main__":
    main()