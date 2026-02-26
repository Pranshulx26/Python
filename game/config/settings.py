
# =============================================================================
# SCREEN SETTINGS
# =============================================================================
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
FPS           = 60
TITLE         = "Breakout"

# =============================================================================
# PADDLE SETTINGS
# =============================================================================
PADDLE_WIDTH    = 100
PADDLE_HEIGHT   = 12
PADDLE_SPEED    = 7
PADDLE_Y_OFFSET = 40

# =============================================================================
# BALL SETTINGS
# =============================================================================
BALL_RADIUS  = 8
BALL_SPEED_X = 4
BALL_SPEED_Y = -4

# =============================================================================
# BRICK SETTINGS
# =============================================================================
BRICK_ROWS       = 6
BRICK_COLS       = 10
BRICK_WIDTH      = 70
BRICK_HEIGHT     = 20
BRICK_PADDING    = 5
BRICK_TOP_OFFSET = 60

# =============================================================================
# GAME SETTINGS
# =============================================================================
PLAYER_LIVES   = 3
HIGH_SCORE_FILE = "high_score.txt"



# =============================================================================
# COLORS              R    G    B
# =============================================================================
BACKGROUND_COLOR  = (  0,   0,   0)   # black
BALL_COLOR        = (255, 255, 255)   # white
PADDLE_COLOR      = (255, 255, 255)   # white
HUD_COLOR         = (255, 255, 255)   # white

BRICK_COLOR_STRONG = (255,  50,  50)  # red    — 3 hits
BRICK_COLOR_MEDIUM = (255, 165,   0)  # orange — 2 hits
BRICK_COLOR_WEAK   = ( 50, 205,  50)  # green  — 1 hit

# =============================================================================
# SOUNDS
# =============================================================================
SOUND_WALL_HIT        = "assets/sounds/wall_hit.wav"
SOUND_PADDLE_HIT      = "assets/sounds/paddle_hit.wav"
SOUND_BRICK_HIT       = "assets/sounds/brick_hit.wav"
SOUND_BRICK_DESTROYED = "assets/sounds/brick_destroyed.wav"
SOUND_LIFE_LOST       = "assets/sounds/life_lost.wav"