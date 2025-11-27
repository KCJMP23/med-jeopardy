from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtWidgets import QApplication, QMessageBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QGroupBox, QCheckBox, QSpinBox

import sys
import argparse
import requests
import logging
from simpleaudio._simpleaudio import SimpleaudioError


from jparty.game import Game
from jparty.controller import BuzzerController
from jparty.main_display import DisplayWindow, HostDisplayWindow
from jparty.style import JPartyStyle
from jparty.utils import resource_path
from jparty.logger import qt_exception_hook
from jparty.constants import PORT
from jparty.med_config import MedJeopardyConfig, GameMode, AudienceSize
from jparty.cme_tracking import CMETracker


def check_internet():
    """check internet connection"""
    try:
        requests.get("http://www.j-archive.com/")
    except requests.exceptions.ConnectionError:  # This is the correct syntax
        logging.error("Connection Error")
        QMessageBox.critical(
            None,
            "Cannot connect!",
            "JParty cannot connect to the J-Archive. Please check your internet connection.",
            buttons=QMessageBox.StandardButton.Abort,
            defaultButton=QMessageBox.StandardButton.Abort,
        )
        exit(1)


def permission_error():
    logging.error(f"Cannot access port {PORT}")
    QMessageBox.critical(
        None,
        "Permission Error",
        f"JParty encountered a permissions error when trying to listen on port {PORT}.",
        buttons=QMessageBox.StandardButton.Abort,
        defaultButton=QMessageBox.StandardButton.Abort,
    )


def audio_error():
    logging.error("Cannot access audio device")
    QMessageBox.critical(
        None,
        "Audio error Error",
        "JParty cannot access an audio device.",
        buttons=QMessageBox.StandardButton.Abort,
        defaultButton=QMessageBox.StandardButton.Abort,
    )


def check_second_monitor():
    if len(QApplication.instance().screens()) < 2:
        logging.error("No two monitors")
        QMessageBox.critical(
            None,
            "Two monitors needed!",
            "JParty needs two separate displays. Please attach a second monitor or turn off mirroring and try again.",
            buttons=QMessageBox.StandardButton.Abort,
            defaultButton=QMessageBox.StandardButton.Abort,
        )
        sys.exit(1)


class MedicalSetupDialog(QDialog):
    """Dialog for configuring medical education settings before game start."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Med-Jeopardy Setup")
        self.setMinimumWidth(400)
        self.config = MedJeopardyConfig()
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()

        # Game Mode Selection
        mode_group = QGroupBox("Game Mode")
        mode_layout = QVBoxLayout()

        self.mode_combo = QComboBox()
        self.mode_combo.addItem("Competition - Standard competitive play", GameMode.COMPETITION)
        self.mode_combo.addItem("Learning - Shows rationale after answers", GameMode.LEARNING)
        self.mode_combo.addItem("Team Battle - Team-based competition", GameMode.TEAM_BATTLE)
        self.mode_combo.addItem("Rapid Fire - Quick review mode", GameMode.RAPID_FIRE)
        mode_layout.addWidget(self.mode_combo)
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)

        # Audience Size
        audience_group = QGroupBox("Audience Size")
        audience_layout = QVBoxLayout()

        self.audience_combo = QComboBox()
        self.audience_combo.addItem("Small Group (1-8 players)", AudienceSize.SMALL_GROUP)
        self.audience_combo.addItem("Medium (9-25 players) - Resident Conference", AudienceSize.MEDIUM)
        self.audience_combo.addItem("Large (26-100 players) - Grand Rounds", AudienceSize.LARGE)
        self.audience_combo.addItem("Virtual Event (100+ players) - CME Webinar", AudienceSize.VIRTUAL_EVENT)
        audience_layout.addWidget(self.audience_combo)
        audience_group.setLayout(audience_layout)
        layout.addWidget(audience_group)

        # Educational Features
        edu_group = QGroupBox("Educational Features")
        edu_layout = QVBoxLayout()

        self.rationale_check = QCheckBox("Show rationale after answers")
        self.rationale_check.setChecked(False)
        edu_layout.addWidget(self.rationale_check)

        self.difficulty_check = QCheckBox("Show difficulty indicators")
        self.difficulty_check.setChecked(True)
        edu_layout.addWidget(self.difficulty_check)

        self.tracking_check = QCheckBox("Track performance for CME/CE")
        self.tracking_check.setChecked(False)
        edu_layout.addWidget(self.tracking_check)

        edu_group.setLayout(edu_layout)
        layout.addWidget(edu_group)

        # Timer Settings
        timer_group = QGroupBox("Timer Settings (seconds)")
        timer_layout = QHBoxLayout()

        timer_layout.addWidget(QLabel("Standard:"))
        self.standard_timer = QSpinBox()
        self.standard_timer.setRange(3, 30)
        self.standard_timer.setValue(8)
        timer_layout.addWidget(self.standard_timer)

        timer_layout.addWidget(QLabel("Case:"))
        self.case_timer = QSpinBox()
        self.case_timer.setRange(5, 60)
        self.case_timer.setValue(15)
        timer_layout.addWidget(self.case_timer)

        timer_layout.addWidget(QLabel("Final:"))
        self.final_timer = QSpinBox()
        self.final_timer.setRange(30, 120)
        self.final_timer.setValue(60)
        timer_layout.addWidget(self.final_timer)

        timer_group.setLayout(timer_layout)
        layout.addWidget(timer_group)

        # Preset buttons
        preset_group = QGroupBox("Quick Presets")
        preset_layout = QHBoxLayout()

        boards_btn = QPushButton("Board Study")
        boards_btn.clicked.connect(self._apply_boards_preset)
        preset_layout.addWidget(boards_btn)

        gme_btn = QPushButton("GME Conference")
        gme_btn.clicked.connect(self._apply_gme_preset)
        preset_layout.addWidget(gme_btn)

        cme_btn = QPushButton("CME Event")
        cme_btn.clicked.connect(self._apply_cme_preset)
        preset_layout.addWidget(cme_btn)

        preset_group.setLayout(preset_layout)
        layout.addWidget(preset_group)

        # Buttons
        button_layout = QHBoxLayout()
        start_btn = QPushButton("Start Game")
        start_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(start_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def _apply_boards_preset(self):
        """Apply board study preset."""
        self.mode_combo.setCurrentIndex(1)  # Learning mode
        self.audience_combo.setCurrentIndex(0)  # Small group
        self.rationale_check.setChecked(True)
        self.difficulty_check.setChecked(True)
        self.tracking_check.setChecked(True)
        self.standard_timer.setValue(15)
        self.case_timer.setValue(30)
        self.final_timer.setValue(90)

    def _apply_gme_preset(self):
        """Apply GME conference preset."""
        self.mode_combo.setCurrentIndex(2)  # Team battle
        self.audience_combo.setCurrentIndex(1)  # Medium
        self.rationale_check.setChecked(True)
        self.difficulty_check.setChecked(True)
        self.tracking_check.setChecked(False)
        self.standard_timer.setValue(8)
        self.case_timer.setValue(15)
        self.final_timer.setValue(60)

    def _apply_cme_preset(self):
        """Apply CME event preset."""
        self.mode_combo.setCurrentIndex(2)  # Team battle
        self.audience_combo.setCurrentIndex(2)  # Large
        self.rationale_check.setChecked(True)
        self.difficulty_check.setChecked(True)
        self.tracking_check.setChecked(True)
        self.standard_timer.setValue(10)
        self.case_timer.setValue(20)
        self.final_timer.setValue(60)

    def get_config(self) -> MedJeopardyConfig:
        """Build and return the configuration based on dialog selections."""
        config = MedJeopardyConfig()

        # Game mode
        config.game_mode = self.mode_combo.currentData()

        # Audience size
        config.audience_size = self.audience_combo.currentData()
        config.apply_audience_preset()

        # Educational features
        config.show_rationale = self.rationale_check.isChecked()
        config.show_difficulty = self.difficulty_check.isChecked()
        config.track_performance = self.tracking_check.isChecked()

        # Enable CME tracking if selected
        if self.tracking_check.isChecked():
            config.cme_tracking.enabled = True

        # Timer settings
        config.timers.standard_question = self.standard_timer.value()
        config.timers.complex_case = self.case_timer.value()
        config.timers.final_jeopardy = self.final_timer.value()

        # Apply game mode specific settings
        config.apply_game_mode()

        return config


def parse_args():
    """Parse command-line arguments for medical education modes."""
    parser = argparse.ArgumentParser(description="Med-Jeopardy - Medical Education Game Platform")

    parser.add_argument(
        "--mode",
        choices=["competition", "learning", "team", "rapid"],
        default=None,
        help="Game mode preset"
    )
    parser.add_argument(
        "--preset",
        choices=["boards", "gme", "grand-rounds", "cme"],
        default=None,
        help="Quick preset for common use cases"
    )
    parser.add_argument(
        "--no-setup",
        action="store_true",
        help="Skip setup dialog and use defaults"
    )
    parser.add_argument(
        "--cme-tracking",
        action="store_true",
        help="Enable CME/CE tracking"
    )

    return parser.parse_args()


def get_config_from_args(args) -> MedJeopardyConfig:
    """Build configuration from command-line arguments."""
    if args.preset:
        presets = {
            "boards": MedJeopardyConfig.for_boards_study,
            "gme": MedJeopardyConfig.for_residency_conference,
            "grand-rounds": MedJeopardyConfig.for_grand_rounds,
            "cme": MedJeopardyConfig.for_virtual_cme,
        }
        config = presets[args.preset]()
    else:
        config = MedJeopardyConfig()

    if args.mode:
        modes = {
            "competition": GameMode.COMPETITION,
            "learning": GameMode.LEARNING,
            "team": GameMode.TEAM_BATTLE,
            "rapid": GameMode.RAPID_FIRE,
        }
        config.game_mode = modes[args.mode]
        config.apply_game_mode()

    if args.cme_tracking:
        config.cme_tracking.enabled = True
        config.track_performance = True

    return config


def main():

    # Parse command-line arguments first
    args = parse_args()

    QApplication.setStyle(JPartyStyle())
    app = QApplication(sys.argv)

    check_second_monitor()
    check_internet()
    app.setFont(QFont("Verdana"))

    QFontDatabase.addApplicationFont(resource_path("ITC_ Korinna Normal.ttf"))

    # Get configuration
    config = None
    cme_tracker = None

    if args.preset or args.no_setup:
        # Use command-line configuration
        config = get_config_from_args(args)
        logging.info(f"Using preset configuration: {args.preset or 'default'}")
    else:
        # Show setup dialog
        setup_dialog = MedicalSetupDialog()
        if setup_dialog.exec() == QDialog.DialogCode.Accepted:
            config = setup_dialog.get_config()
            logging.info(f"Configuration: mode={config.game_mode.value}, audience={config.audience_size.value}")
        else:
            # User cancelled - use default config
            config = MedJeopardyConfig()
            logging.info("Using default configuration")

    # Initialize CME tracker if enabled
    if config.cme_tracking.enabled:
        cme_tracker = CMETracker(config)
        cme_tracker.start_session()
        logging.info("CME tracking enabled")

    # Create game with configuration
    game = Game(config)
    game.cme_tracker = cme_tracker  # Attach tracker to game

    socket_controller = BuzzerController(game, config)

    game.setBuzzerController(socket_controller)

    try:
        socket_controller.start()
    except PermissionError:
        permission_error()
        exit(1)

    main_window = DisplayWindow(game)
    host_window = HostDisplayWindow(game)
    game.setDisplays(host_window, main_window)

    try:
        game.begin_theme_song()
    except SimpleaudioError:
        audio_error()
        exit(1)

    song_player = game.song_player

    r = 1  # fail by default
    try:
        r = app.exec()
    finally:
        logging.info("terminated")

        # Export CME report if tracking was enabled
        if cme_tracker:
            cme_tracker.end_session()
            cme_tracker.update_final_scores(game.players)
            try:
                cme_tracker.export_csv("med_jeopardy_session_report.csv")
                logging.info("CME report exported to med_jeopardy_session_report.csv")
            except Exception as e:
                logging.error(f"Failed to export CME report: {e}")

        if song_player:
            song_player.stop()

        sys.exit(r)
