import pygame
from typing import Optional, List
from config import settings
from config.controls import (    
    KEY_PADDLE_LEFT,
    KEY_PADDLE_RIGHT,
    KEY_PAUSE,
    KEY_QUIT
)


class InputHandler:
    """
    Translates raw pygame input into clean game commands.
    GameEngine never touches pygame input directly.
    """

    def get_events(self) -> List[pygame.event.Event]:
        """
        Return all pygame events this frame.
        Called once per frame by GameEngine.
        """
        return pygame.event.get()

    def get_paddle_direction(self) -> Optional[str]:
        """
        Return paddle direction based on held keys.
        Returns 'left', 'right', or None.
        State-based — checked every frame.
        """
        keys = pygame.key.get_pressed()

        if keys[KEY_PADDLE_LEFT]:
            return "left"
        if keys[KEY_PADDLE_RIGHT]:
            return "right"

        return None

    def __repr__(self) -> str:
        return "InputHandler()"