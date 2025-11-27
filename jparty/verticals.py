"""
Vertical-specific configuration for Med-Jeopardy deployments.

Each vertical (Boards, GME, CME) has its own branding, defaults, and features.
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class Vertical(Enum):
    """Available deployment verticals."""
    BOARDS = "boards"      # Board exam preparation
    GME = "gme"            # Graduate Medical Education
    CME = "cme"            # Continuing Medical Education
    GENERIC = "generic"    # Generic medical jeopardy


@dataclass
class VerticalConfig:
    """Configuration for a specific vertical deployment."""
    vertical: Vertical
    app_name: str
    app_title: str
    tagline: str
    primary_color: str
    secondary_color: str
    default_categories: List[str]
    features: List[str]
    disabled_features: List[str]
    help_url: Optional[str] = None
    support_email: Optional[str] = None


# Board Study Vertical Configuration
BOARDS_CONFIG = VerticalConfig(
    vertical=Vertical.BOARDS,
    app_name="MedJeopardy-Boards",
    app_title="Med-Jeopardy: Board Study",
    tagline="Master the Boards, One Question at a Time",
    primary_color="#1565C0",  # Blue (study/academic)
    secondary_color="#42A5F5",
    default_categories=[
        "Cardiology",
        "Pulmonology",
        "Gastroenterology",
        "Nephrology",
        "Neurology",
        "Pharmacology"
    ],
    features=[
        "learning_mode",
        "rationale_display",
        "difficulty_indicators",
        "performance_tracking",
        "spaced_repetition",
        "high_yield_tags",
        "first_aid_references"
    ],
    disabled_features=[
        "cme_tracking",
        "certificate_generation",
        "team_mode"
    ],
    help_url="https://docs.onehealth.io/medjeopardy/boards"
)

# GME/Residency Vertical Configuration
GME_CONFIG = VerticalConfig(
    vertical=Vertical.GME,
    app_name="MedJeopardy-GME",
    app_title="Med-Jeopardy: GME Edition",
    tagline="Interactive Learning for Residency Training",
    primary_color="#2E7D32",  # Green (growth/education)
    secondary_color="#66BB6A",
    default_categories=[
        "Morning Report",
        "Case Conference",
        "M&M Review",
        "Evidence-Based Medicine",
        "Quality Improvement",
        "Patient Safety"
    ],
    features=[
        "team_mode",
        "rationale_display",
        "difficulty_indicators",
        "case_vignettes",
        "image_support",
        "milestone_mapping",
        "competency_tracking"
    ],
    disabled_features=[
        "cme_tracking",
        "spaced_repetition"
    ],
    help_url="https://docs.onehealth.io/medjeopardy/gme"
)

# CME/CE Vertical Configuration
CME_CONFIG = VerticalConfig(
    vertical=Vertical.CME,
    app_name="MedJeopardy-CME",
    app_title="Med-Jeopardy: CME Edition",
    tagline="Engaging CME for Healthcare Professionals",
    primary_color="#6A1B9A",  # Purple (professional/premium)
    secondary_color="#AB47BC",
    default_categories=[
        "Updates in Practice",
        "Guidelines Review",
        "Case Studies",
        "New Treatments",
        "Quality Metrics",
        "Hot Topics"
    ],
    features=[
        "cme_tracking",
        "certificate_generation",
        "attendance_tracking",
        "team_mode",
        "large_audience",
        "spectator_mode",
        "rationale_display",
        "export_reports"
    ],
    disabled_features=[
        "spaced_repetition",
        "high_yield_tags"
    ],
    help_url="https://docs.onehealth.io/medjeopardy/cme"
)

# Generic Medical Jeopardy Configuration
GENERIC_CONFIG = VerticalConfig(
    vertical=Vertical.GENERIC,
    app_name="MedJeopardy",
    app_title="Med-Jeopardy",
    tagline="Medical Education Through Gamification",
    primary_color="#1010a1",  # Original Jeopardy blue
    secondary_color="#0b0b74",
    default_categories=[
        "Anatomy",
        "Physiology",
        "Pathology",
        "Pharmacology",
        "Microbiology",
        "Biochemistry"
    ],
    features=[
        "learning_mode",
        "team_mode",
        "rationale_display",
        "difficulty_indicators",
        "image_support",
        "cme_tracking"
    ],
    disabled_features=[],
    help_url="https://docs.onehealth.io/medjeopardy"
)


def get_vertical_config(vertical: Vertical) -> VerticalConfig:
    """Get configuration for a specific vertical."""
    configs = {
        Vertical.BOARDS: BOARDS_CONFIG,
        Vertical.GME: GME_CONFIG,
        Vertical.CME: CME_CONFIG,
        Vertical.GENERIC: GENERIC_CONFIG,
    }
    return configs.get(vertical, GENERIC_CONFIG)


def get_vertical_from_preset(preset: str) -> Vertical:
    """Map preset name to vertical."""
    mapping = {
        "boards": Vertical.BOARDS,
        "gme": Vertical.GME,
        "grand-rounds": Vertical.CME,
        "cme": Vertical.CME,
    }
    return mapping.get(preset, Vertical.GENERIC)


# Feature flags for each vertical
FEATURE_DESCRIPTIONS = {
    "learning_mode": "Educational mode with rationale and second chances",
    "team_mode": "Team-based collaborative competition",
    "rationale_display": "Show educational explanations after answers",
    "difficulty_indicators": "Display question difficulty levels",
    "performance_tracking": "Track individual performance metrics",
    "spaced_repetition": "Schedule review of missed questions",
    "high_yield_tags": "Mark high-yield board exam topics",
    "first_aid_references": "Link to First Aid/review resources",
    "cme_tracking": "Track CME/CE credit eligibility",
    "certificate_generation": "Generate CME completion certificates",
    "attendance_tracking": "Track participant attendance",
    "large_audience": "Support 100+ concurrent players",
    "spectator_mode": "Allow non-playing viewers",
    "case_vignettes": "Extended clinical case scenarios",
    "image_support": "Display clinical images (X-ray, CT, etc.)",
    "milestone_mapping": "Map to ACGME milestones",
    "competency_tracking": "Track competency development",
    "export_reports": "Export session data for reporting",
}
