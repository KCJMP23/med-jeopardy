"""
Medical Education Configuration for Med-Jeopardy

This module provides configuration options for medical education use cases:
1. Board exam study (USMLE, COMLEX, specialty boards)
2. Graduate Medical Education (GME) - residency training
3. CME/CE events (grand rounds, dinner meetings, virtual events)
"""

from dataclasses import dataclass, field
from typing import Optional, List
from enum import Enum
import json


class GameMode(Enum):
    """Game modes optimized for different medical education contexts."""
    COMPETITION = "competition"      # Standard competitive play
    LEARNING = "learning"            # Educational mode with explanations
    TEAM_BATTLE = "team_battle"      # Team-based competition
    RAPID_FIRE = "rapid_fire"        # Quick review mode


class AudienceSize(Enum):
    """Preset configurations for different audience sizes."""
    SMALL_GROUP = "small"       # 1-8 players (study group, small didactic)
    MEDIUM = "medium"           # 9-25 players (resident conference)
    LARGE = "large"             # 26-100 players (grand rounds)
    VIRTUAL_EVENT = "virtual"   # 100+ players (CME/CE webinars)


class DifficultyLevel(Enum):
    """Difficulty levels for medical questions."""
    BASIC = "basic"             # Medical student level
    INTERMEDIATE = "intermediate"  # Intern/resident level
    ADVANCED = "advanced"       # Fellow/attending level
    EXPERT = "expert"          # Board exam level


@dataclass
class TimerConfig:
    """Configurable timer settings for medical questions."""
    standard_question: int = 8      # Seconds for standard questions (longer than TV)
    complex_case: int = 15          # Seconds for complex case vignettes
    image_question: int = 12        # Seconds for image-based questions
    final_jeopardy: int = 60        # Seconds for Final Jeopardy
    buzzer_delay: float = 0.25      # Delay before accepting buzzes (seconds)

    @classmethod
    def for_mode(cls, mode: GameMode) -> 'TimerConfig':
        """Get timer configuration for a specific game mode."""
        if mode == GameMode.RAPID_FIRE:
            return cls(
                standard_question=5,
                complex_case=8,
                image_question=6,
                final_jeopardy=30,
                buzzer_delay=0.15
            )
        elif mode == GameMode.LEARNING:
            return cls(
                standard_question=15,
                complex_case=30,
                image_question=20,
                final_jeopardy=90,
                buzzer_delay=0.5
            )
        return cls()


@dataclass
class PointConfig:
    """Configurable point values for medical education."""
    # Standard round values (can represent difficulty or CME points)
    round_1: List[int] = field(default_factory=lambda: [100, 200, 300, 400, 500])
    round_2: List[int] = field(default_factory=lambda: [200, 400, 600, 800, 1000])

    # Alternative: CME-style point values
    @classmethod
    def cme_style(cls) -> 'PointConfig':
        """Point values representing CME credit fractions."""
        return cls(
            round_1=[1, 2, 3, 4, 5],
            round_2=[2, 4, 6, 8, 10]
        )

    @classmethod
    def standard(cls) -> 'PointConfig':
        """Standard Jeopardy-style dollar values."""
        return cls(
            round_1=[200, 400, 600, 800, 1000],
            round_2=[400, 800, 1200, 1600, 2000]
        )


@dataclass
class TeamConfig:
    """Configuration for team-based play."""
    enabled: bool = False
    max_teams: int = 8
    players_per_team: int = 5
    team_names: List[str] = field(default_factory=list)
    allow_conferring: bool = True  # Allow team discussion before answering
    conferring_time: int = 10      # Additional seconds for team discussion


@dataclass
class MedicalCategory:
    """Medical category with specialty tagging."""
    name: str
    specialty: str = ""           # e.g., "Cardiology", "Neurology"
    system: str = ""              # e.g., "Cardiovascular", "Nervous"
    difficulty: DifficultyLevel = DifficultyLevel.INTERMEDIATE

    def display_name(self) -> str:
        """Get display name with optional specialty tag."""
        if self.specialty:
            return f"{self.name}\n({self.specialty})"
        return self.name


@dataclass
class CMETrackingConfig:
    """Configuration for CME/CE credit tracking."""
    enabled: bool = False
    event_name: str = ""
    event_date: str = ""
    institution: str = ""
    credit_type: str = "AMA PRA Category 1"  # or "AAFP", "ANCC", etc.
    credits_available: float = 1.0
    track_attendance: bool = True
    require_minimum_participation: bool = True
    minimum_questions_answered: int = 5
    export_format: str = "csv"  # "csv", "json", "pdf"


@dataclass
class MedJeopardyConfig:
    """Main configuration class for Med-Jeopardy."""
    # Game mode settings
    game_mode: GameMode = GameMode.COMPETITION
    audience_size: AudienceSize = AudienceSize.SMALL_GROUP

    # Player capacity (dynamically adjusted based on audience size)
    max_players: int = 8
    allow_spectators: bool = False

    # Timer configuration
    timers: TimerConfig = field(default_factory=TimerConfig)

    # Point configuration
    points: PointConfig = field(default_factory=PointConfig)

    # Team configuration
    teams: TeamConfig = field(default_factory=TeamConfig)

    # Educational features
    show_rationale: bool = False      # Show explanation after answer
    show_difficulty: bool = True      # Show difficulty indicator
    track_performance: bool = True    # Track individual performance
    allow_second_chance: bool = False # Allow retry on missed questions (learning mode)

    # CME/CE tracking
    cme_tracking: CMETrackingConfig = field(default_factory=CMETrackingConfig)

    # Display options
    show_category_tags: bool = True   # Show specialty/system tags
    use_medical_theme: bool = True    # Use medical-themed styling
    institution_logo: Optional[str] = None  # Path to institution logo

    # Media support
    support_images: bool = True       # Allow image-based questions
    support_audio: bool = False       # Allow audio clips (heart sounds, etc.)
    image_display_time: int = 5       # Extra seconds when image is shown

    def apply_audience_preset(self):
        """Apply preset settings based on audience size."""
        if self.audience_size == AudienceSize.SMALL_GROUP:
            self.max_players = 8
            self.teams.enabled = False
        elif self.audience_size == AudienceSize.MEDIUM:
            self.max_players = 25
            self.teams.enabled = True
            self.teams.max_teams = 5
            self.teams.players_per_team = 5
        elif self.audience_size == AudienceSize.LARGE:
            self.max_players = 100
            self.teams.enabled = True
            self.teams.max_teams = 10
            self.teams.players_per_team = 10
        elif self.audience_size == AudienceSize.VIRTUAL_EVENT:
            self.max_players = 500
            self.teams.enabled = True
            self.teams.max_teams = 50
            self.teams.players_per_team = 10
            self.allow_spectators = True

    def apply_game_mode(self):
        """Apply settings based on game mode."""
        self.timers = TimerConfig.for_mode(self.game_mode)

        if self.game_mode == GameMode.LEARNING:
            self.show_rationale = True
            self.allow_second_chance = True
            self.track_performance = True
        elif self.game_mode == GameMode.TEAM_BATTLE:
            self.teams.enabled = True

    @classmethod
    def for_boards_study(cls) -> 'MedJeopardyConfig':
        """Preset for board exam study sessions."""
        config = cls(
            game_mode=GameMode.LEARNING,
            audience_size=AudienceSize.SMALL_GROUP,
            show_rationale=True,
            show_difficulty=True,
            track_performance=True,
            allow_second_chance=True
        )
        config.apply_audience_preset()
        config.apply_game_mode()
        return config

    @classmethod
    def for_residency_conference(cls) -> 'MedJeopardyConfig':
        """Preset for residency/GME conference."""
        config = cls(
            game_mode=GameMode.COMPETITION,
            audience_size=AudienceSize.MEDIUM,
            show_rationale=True,
            show_difficulty=True,
            teams=TeamConfig(enabled=True, max_teams=5)
        )
        config.apply_audience_preset()
        return config

    @classmethod
    def for_grand_rounds(cls) -> 'MedJeopardyConfig':
        """Preset for grand rounds / CME events."""
        config = cls(
            game_mode=GameMode.TEAM_BATTLE,
            audience_size=AudienceSize.LARGE,
            show_rationale=True,
            cme_tracking=CMETrackingConfig(enabled=True),
            allow_spectators=True
        )
        config.apply_audience_preset()
        config.apply_game_mode()
        return config

    @classmethod
    def for_virtual_cme(cls) -> 'MedJeopardyConfig':
        """Preset for virtual CME/CE events."""
        config = cls(
            game_mode=GameMode.TEAM_BATTLE,
            audience_size=AudienceSize.VIRTUAL_EVENT,
            show_rationale=True,
            cme_tracking=CMETrackingConfig(
                enabled=True,
                track_attendance=True,
                require_minimum_participation=True
            ),
            allow_spectators=True
        )
        config.apply_audience_preset()
        config.apply_game_mode()
        return config

    def to_json(self) -> str:
        """Export configuration to JSON."""
        return json.dumps(self.__dict__, default=str, indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> 'MedJeopardyConfig':
        """Import configuration from JSON."""
        data = json.loads(json_str)
        config = cls()
        # Apply loaded values
        for key, value in data.items():
            if hasattr(config, key):
                setattr(config, key, value)
        return config


# Default configuration instance
DEFAULT_CONFIG = MedJeopardyConfig()

# Medical specialty categories for tagging
MEDICAL_SPECIALTIES = [
    "Internal Medicine",
    "Family Medicine",
    "Pediatrics",
    "Surgery",
    "Obstetrics & Gynecology",
    "Psychiatry",
    "Neurology",
    "Emergency Medicine",
    "Anesthesiology",
    "Radiology",
    "Pathology",
    "Dermatology",
    "Ophthalmology",
    "Otolaryngology",
    "Orthopedics",
    "Urology",
    "Cardiology",
    "Pulmonology",
    "Gastroenterology",
    "Nephrology",
    "Endocrinology",
    "Rheumatology",
    "Infectious Disease",
    "Oncology",
    "Hematology",
    "Allergy & Immunology",
    "Physical Medicine",
    "Preventive Medicine",
    "Pharmacology",
    "Biostatistics & Epidemiology",
]

# Organ systems for question categorization
ORGAN_SYSTEMS = [
    "Cardiovascular",
    "Respiratory",
    "Gastrointestinal",
    "Renal/Urinary",
    "Reproductive",
    "Musculoskeletal",
    "Nervous",
    "Integumentary",
    "Endocrine",
    "Hematologic/Lymphatic",
    "Immune",
    "Multisystem",
]
