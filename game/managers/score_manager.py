# managers/score_manager.py

from config import settings


class ScoreManager:
    """
    Handles high score persistence.
    Reads and writes to file — game state stays separate.
    """

    def __init__(self):
        self._high_score = self._load_high_score()

    def get_high_score(self) -> int:
        """Return current high score."""
        return self._high_score

    def update_high_score(self, score: int) -> bool:
        """
        Compare score against high score.
        Saves and returns True if new high score achieved.
        """
        if score > self._high_score:
            self._high_score = score
            self._save_high_score(score)
            return True
        return False

    def _load_high_score(self) -> int:
        """
        Load high score from file.
        Returns 0 if file missing — first time running game.
        """
        try:
            with open(settings.HIGH_SCORE_FILE, "r") as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def _save_high_score(self, score: int) -> None:
        """
        Save new high score to file.
        Fails gracefully — never crashes game over file error.
        """
        try:
            with open(settings.HIGH_SCORE_FILE, "w") as f:
                f.write(str(score))
        except IOError as e:
            print(f"Warning: Could not save high score: {e}")

    def __repr__(self) -> str:
        return f"ScoreManager(high_score={self._high_score})"