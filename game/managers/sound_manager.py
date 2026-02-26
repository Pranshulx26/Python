# managers/sound_manager.py

import pygame
from config import settings


class SoundManager:
    """
    Loads and plays all game sounds.
    Handles missing sound files gracefully — game continues without sound.
    """

    def __init__(self):
        self._sounds = {}
        self._enabled = True
        self._load_sounds()

    def _load_sounds(self) -> None:
        """
        Load all sounds at startup.
        If sound file missing — log warning, continue silently.
        """
        sound_files = {
            "wall_hit":        settings.SOUND_WALL_HIT,
            "paddle_hit":      settings.SOUND_PADDLE_HIT,
            "brick_hit":       settings.SOUND_BRICK_HIT,
            "brick_destroyed": settings.SOUND_BRICK_DESTROYED,
            "life_lost":       settings.SOUND_LIFE_LOST,
        }

        for name, filepath in sound_files.items():
            try:
                self._sounds[name] = pygame.mixer.Sound(filepath)
            except FileNotFoundError:
                print(f"Warning: Sound '{name}' not found at {filepath}")
                self._sounds[name] = None

    def play(self, name: str) -> None:
        """
        Play sound by name.
        Fails silently if sound missing or disabled — never crashes game.
        """
        if not self._enabled:
            return

        sound = self._sounds.get(name)
        if sound:
            sound.play()

    def toggle(self) -> None:
        """Mute/unmute all sounds."""
        self._enabled = not self._enabled

    def __repr__(self) -> str:
        return f"SoundManager(enabled={self._enabled})"