"""
CME/CE Tracking and Export Module for Med-Jeopardy

Provides functionality to:
1. Track participant performance during sessions
2. Generate CME/CE attendance and completion reports
3. Export data for credit claiming purposes
"""

import csv
import json
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
import logging


@dataclass
class ParticipantRecord:
    """Record of a participant's session performance."""
    name: str
    team: Optional[str] = None
    questions_answered: int = 0
    questions_correct: int = 0
    final_score: int = 0
    specialty_breakdown: Dict[str, Dict[str, int]] = field(default_factory=dict)
    joined_at: str = ""
    completed: bool = False

    def accuracy(self) -> float:
        """Calculate accuracy percentage."""
        if self.questions_answered == 0:
            return 0.0
        return (self.questions_correct / self.questions_answered) * 100

    def meets_minimum_participation(self, min_questions: int) -> bool:
        """Check if participant meets minimum participation requirement."""
        return self.questions_answered >= min_questions


@dataclass
class TeamRecord:
    """Record of a team's session performance."""
    name: str
    members: List[str] = field(default_factory=list)
    total_score: int = 0
    questions_answered: int = 0
    questions_correct: int = 0

    def accuracy(self) -> float:
        """Calculate team accuracy percentage."""
        if self.questions_answered == 0:
            return 0.0
        return (self.questions_correct / self.questions_answered) * 100


@dataclass
class SessionReport:
    """Complete session report for CME/CE tracking."""
    event_name: str
    event_date: str
    institution: str
    credit_type: str
    credits_available: float
    session_start: str
    session_end: str
    total_questions: int
    questions_played: int
    participants: List[ParticipantRecord] = field(default_factory=list)
    teams: List[TeamRecord] = field(default_factory=list)
    categories_covered: List[str] = field(default_factory=list)
    specialties_covered: List[str] = field(default_factory=list)


class CMETracker:
    """
    Tracks CME/CE session data and generates reports.

    Usage:
        tracker = CMETracker(config)
        tracker.start_session()
        tracker.record_participant(player)
        tracker.record_answer(player, question, correct)
        report = tracker.generate_report()
        tracker.export_csv("session_report.csv")
    """

    def __init__(self, config=None):
        """Initialize CME tracker with configuration."""
        self.config = config
        self.session_start = None
        self.session_end = None
        self.participants: Dict[str, ParticipantRecord] = {}
        self.teams: Dict[str, TeamRecord] = {}
        self.questions_played = 0
        self.total_questions = 0
        self.categories_covered = set()
        self.specialties_covered = set()

    def start_session(self):
        """Mark the start of a CME session."""
        self.session_start = datetime.now().isoformat()
        logging.info(f"CME session started at {self.session_start}")

    def end_session(self):
        """Mark the end of a CME session."""
        self.session_end = datetime.now().isoformat()
        for participant in self.participants.values():
            participant.completed = True
        logging.info(f"CME session ended at {self.session_end}")

    def record_participant(self, player):
        """Record a new participant in the session."""
        if player.name not in self.participants:
            team = getattr(player, 'team', None)
            self.participants[player.name] = ParticipantRecord(
                name=player.name,
                team=team,
                joined_at=datetime.now().isoformat()
            )

            # Record team membership if in team mode
            if team:
                if team not in self.teams:
                    self.teams[team] = TeamRecord(name=team)
                self.teams[team].members.append(player.name)

            logging.info(f"CME: Recorded participant {player.name}")

    def record_answer(self, player, question, correct: bool):
        """Record an answer attempt for CME tracking."""
        if player.name not in self.participants:
            self.record_participant(player)

        participant = self.participants[player.name]
        participant.questions_answered += 1
        if correct:
            participant.questions_correct += 1

        # Track specialty breakdown
        if question.specialty:
            self.specialties_covered.add(question.specialty)
            if question.specialty not in participant.specialty_breakdown:
                participant.specialty_breakdown[question.specialty] = {"correct": 0, "total": 0}
            participant.specialty_breakdown[question.specialty]["total"] += 1
            if correct:
                participant.specialty_breakdown[question.specialty]["correct"] += 1

        # Track categories
        if question.category:
            self.categories_covered.add(question.category)

        # Update team stats if applicable
        if participant.team and participant.team in self.teams:
            team = self.teams[participant.team]
            team.questions_answered += 1
            if correct:
                team.questions_correct += 1

        self.questions_played += 1

    def update_final_scores(self, players):
        """Update final scores for all participants."""
        for player in players:
            if player.name in self.participants:
                self.participants[player.name].final_score = player.score
                if player.team and player.team in self.teams:
                    # Aggregate team scores
                    self.teams[player.team].total_score = sum(
                        self.participants[m].final_score
                        for m in self.teams[player.team].members
                        if m in self.participants
                    )

    def generate_report(self) -> SessionReport:
        """Generate a complete CME session report."""
        cme_config = getattr(self.config, 'cme_tracking', None)

        return SessionReport(
            event_name=cme_config.event_name if cme_config else "Medical Jeopardy Session",
            event_date=cme_config.event_date if cme_config else datetime.now().strftime("%Y-%m-%d"),
            institution=cme_config.institution if cme_config else "",
            credit_type=cme_config.credit_type if cme_config else "AMA PRA Category 1",
            credits_available=cme_config.credits_available if cme_config else 1.0,
            session_start=self.session_start or "",
            session_end=self.session_end or datetime.now().isoformat(),
            total_questions=self.total_questions,
            questions_played=self.questions_played,
            participants=list(self.participants.values()),
            teams=list(self.teams.values()),
            categories_covered=list(self.categories_covered),
            specialties_covered=list(self.specialties_covered)
        )

    def get_eligible_participants(self, min_questions: int = 5) -> List[ParticipantRecord]:
        """Get list of participants who meet minimum participation requirements."""
        return [
            p for p in self.participants.values()
            if p.meets_minimum_participation(min_questions)
        ]

    def export_csv(self, filepath: str):
        """Export session data to CSV for CME credit processing."""
        report = self.generate_report()

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Header information
            writer.writerow(["CME Session Report"])
            writer.writerow(["Event Name", report.event_name])
            writer.writerow(["Event Date", report.event_date])
            writer.writerow(["Institution", report.institution])
            writer.writerow(["Credit Type", report.credit_type])
            writer.writerow(["Credits Available", report.credits_available])
            writer.writerow(["Session Start", report.session_start])
            writer.writerow(["Session End", report.session_end])
            writer.writerow([])

            # Participant data
            writer.writerow(["PARTICIPANT DATA"])
            writer.writerow([
                "Name", "Team", "Questions Answered", "Questions Correct",
                "Accuracy %", "Final Score", "CME Eligible", "Completed"
            ])

            cme_config = getattr(self.config, 'cme_tracking', None)
            min_questions = getattr(cme_config, 'minimum_questions_answered', 5) if cme_config else 5

            for p in report.participants:
                writer.writerow([
                    p.name,
                    p.team or "N/A",
                    p.questions_answered,
                    p.questions_correct,
                    f"{p.accuracy():.1f}%",
                    p.final_score,
                    "Yes" if p.meets_minimum_participation(min_questions) else "No",
                    "Yes" if p.completed else "No"
                ])

            writer.writerow([])

            # Team data (if applicable)
            if report.teams:
                writer.writerow(["TEAM DATA"])
                writer.writerow([
                    "Team Name", "Members", "Total Score", "Questions Answered",
                    "Questions Correct", "Accuracy %"
                ])
                for t in report.teams:
                    writer.writerow([
                        t.name,
                        len(t.members),
                        t.total_score,
                        t.questions_answered,
                        t.questions_correct,
                        f"{t.accuracy():.1f}%"
                    ])

            writer.writerow([])

            # Summary
            writer.writerow(["SESSION SUMMARY"])
            writer.writerow(["Total Participants", len(report.participants)])
            writer.writerow(["CME Eligible Participants", len(self.get_eligible_participants(min_questions))])
            writer.writerow(["Questions Played", report.questions_played])
            writer.writerow(["Categories Covered", ", ".join(report.categories_covered)])
            writer.writerow(["Specialties Covered", ", ".join(report.specialties_covered)])

        logging.info(f"CME report exported to {filepath}")

    def export_json(self, filepath: str):
        """Export session data to JSON format."""
        report = self.generate_report()

        # Convert dataclasses to dicts for JSON serialization
        data = {
            "event_info": {
                "name": report.event_name,
                "date": report.event_date,
                "institution": report.institution,
                "credit_type": report.credit_type,
                "credits_available": report.credits_available
            },
            "session_times": {
                "start": report.session_start,
                "end": report.session_end
            },
            "statistics": {
                "total_questions": report.total_questions,
                "questions_played": report.questions_played,
                "total_participants": len(report.participants),
                "categories_covered": report.categories_covered,
                "specialties_covered": report.specialties_covered
            },
            "participants": [asdict(p) for p in report.participants],
            "teams": [asdict(t) for t in report.teams]
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        logging.info(f"CME report exported to {filepath}")

    def export_attendance_list(self, filepath: str):
        """Export simple attendance list for CME credit claims."""
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Participant Name", "Questions Answered", "CME Eligible"])

            cme_config = getattr(self.config, 'cme_tracking', None)
            min_questions = getattr(cme_config, 'minimum_questions_answered', 5) if cme_config else 5

            for p in self.participants.values():
                writer.writerow([
                    p.name,
                    p.questions_answered,
                    "Yes" if p.meets_minimum_participation(min_questions) else "No"
                ])

        logging.info(f"Attendance list exported to {filepath}")
