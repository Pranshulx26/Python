
import pygame 
from config import settings

class Screen:
    def __init__(self):
        self.surface = pygame.display.set_mode(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        )

        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()

    def tick(self, fps: int) -> None:
        """Controls game speed - called once per frame."""
        self.clock.tick(fps)

    def get_surface(self) -> pygame.Surface:
        """Return drawable surface for Renderer."""
        return self.surface