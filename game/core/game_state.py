
class GameState:

    def __init__(
        self,
        initial_lives: int,
        initial_level: int
    ):

        # -- Dynamic game data
        self.score = 0 
        self.lives = initial_lives
        self.current_level = initial_level
        self.bricks_remaining = 0 

        # -- Game condition flags --
        self.is_paused = False
        self.is_game_over = False
        self.has_won = False

        # -- Store initial values for reset --
        self._initial_lives = initial_lives
        self._initial_level = initial_level

    # ------------------------
    # Score management
    # ------------------------

    def add_score(self, points: int) -> None:
        """Add points to current score."""
        if points < 0:
            raise ValueError('Points cannot be negative')
        self.score += points

    # -------------------------
    # Live Management
    # -------------------------

    def lose_life(self) -> None:
        """
        Reduce lives by one.
        Automatically sets game_over if lives reach zero.
        """
        self.lives -= 1
        if self.lives <= 0:
            self.lives = 0
            self.is_game_over = True

    def is_alive(self) -> bool:
        """Returns whether player still has lives remaining."""

        return self.lives > 0 

    # ---------------------
    # Brick Tracking
    # ---------------------

    def set_brick_count(self, count: int) -> None:
        """Called by LevelManager when level loads."""
        self.bricks_remaining = count

    def brick_destroyed(self) -> None:
        """
        Register a brick destruction.
        Automatically sets has_won if all bricks cleared.
        """

        self.bricks_remaining -= 1
        if self.bricks_remaining <= 0:
            self.bricks_remaining = 0 
            self.has_won = True

    # -------------------------------
    # Level Management
    # -------------------------------

    def advance_level(self) -> None:
        """Move to next level and reest with flag for new level."""
        self.current_level += 1
        self.has_won = False

    # --------------------------------
    # Pause Management
    # --------------------------------

    def toggle_pause(self) -> None:
        """Flip pause state."""
        self.is_paused = not self.is_paused


    # --------------------------------
    # Full Reset
    # --------------------------------

    def reset(self) -> None:
        """Restore game to initial state. Used on new game."""

        self.score = 0
        self.lives = self._initial_lives
        self.current_level = self._initial_level
        self.bricks_remaining = 0 
        self.is_paused = False
        self.is_game_over = False
        self.has_won = False


    def __repr__(self) -> str:
        return (
            f"GameState("
            f"score={self.score}, "
            f"lives={self.lives}, "
            f"level={self.current_level}, "
            f"bricks={self.bricks_remaining}, "
            f"game_over={self.is_game_over}, "
            f"won={self.has_won})"
        )