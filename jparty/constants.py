"""
Constants for Med-Jeopardy

These are the base constants. For medical education settings,
see med_config.py for configurable options.
"""

# Default timing constants (can be overridden by MedJeopardyConfig)
FJTIME = 31                    # Final Jeopardy time (seconds)
QUESTIONTIME = 4               # Standard question time (seconds)
QUESTIONTIME_EXTENDED = 8      # Extended time for complex medical questions
QUESTIONTIME_IMAGE = 12        # Time for image-based questions
QUESTIONTIME_CASE = 15         # Time for case vignettes

# Point values
MONIES = [[200, 400, 600, 800, 1000], [400, 800, 1200, 1600, 2000]]
# Medical education point values (CME-style)
MED_POINTS = [[100, 200, 300, 400, 500], [200, 400, 600, 800, 1000]]

# Player limits - base value (can be extended for large events)
MAXPLAYERS = 8                 # Default max for standard mode
MAXPLAYERS_TEAM = 50           # Max teams for team mode
MAXPLAYERS_LARGE_EVENT = 500   # Max for large CME events

# Network settings
PORT = 8080
BUZZER_DELAY = 0.25            # in seconds

# Animation timing
BEFORE_REVEAL_WAIT_TIME = 100  # in ms
CATEGORY_REVEAL_TIME = 2000    # in ms
QUESTION_REVEAL_TIME = 400     # in ms

# Medical education specific
RATIONALE_DISPLAY_TIME = 5000  # ms to show rationale
TEAM_CONFERRING_TIME = 10      # seconds for team discussion
IMAGE_PRELOAD_TIME = 2000      # ms to preload images
