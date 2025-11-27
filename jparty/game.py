from PyQt6.QtCore import Qt, QObject, pyqtSignal
from PyQt6.QtWidgets import (
    QInputDialog,
    QApplication,
    )

import threading
import time
from dataclasses import dataclass
import os
import sys
import simpleaudio as sa
from collections.abc import Iterable
import logging

from jparty.utils import SongPlayer, resource_path, CompoundObject, DDWagerDialog
from jparty.constants import FJTIME, QUESTIONTIME, BUZZER_DELAY, QUESTIONTIME_EXTENDED, QUESTIONTIME_IMAGE, QUESTIONTIME_CASE
from jparty.med_config import MedJeopardyConfig, GameMode


class QuestionTimer(object):
    def __init__(self, interval, f, *args, **kwargs):
        super().__init__()
        self.f = f
        self.args = args
        self.kwargs = kwargs
        self.interval = interval
        self.__thread = None
        self.__start_time = None
        self.__elapsed_time = 0

    def run(self, i):
        thread = self.__thread
        time.sleep(i)
        if thread == self.__thread:
            self.f(*self.args, **self.kwargs)

    def start(self):
        """wrapper for resume"""
        self.resume()

    def cancel(self):
        """wrapper for pause"""
        self.pause()

    def pause(self):
        self.__thread = None
        self.__elapsed_time += time.time() - self.__start_time

    def resume(self):
        self.__thread = threading.Thread(
            target=self.run, args=(self.interval - self.__elapsed_time,)
        )
        self.__thread.start()
        self.__start_time = time.time()


@dataclass
class KeystrokeEvent:
    key: int
    func: callable
    hint_setter: callable = None
    active: bool = False
    persistent: bool = False


class KeystrokeManager(object):
    def __init__(self):
        super().__init__()
        self.__events = {}

    def addEvent(
        self, ident, key, func, hint_setter=None, active=False, persistent=False
    ):
        self.__events[ident] = KeystrokeEvent(
            key, func, hint_setter, active, persistent
        )

    def call(self, key):
        """this is split in to two for loops so one execution doesnt cause another event to trigger"""
        events_to_call = []
        for ident, event in self.__events.items():
            if event.active and event.key == key:
                logging.info(f"Calling {ident}")
                events_to_call.append(event)
                if not event.persistent:
                    self._deactivate(ident)

        for event in events_to_call:
            event.func()

    def _activate(self, ident):
        logging.info(f"Activating {ident}")
        e = self.__events[ident]
        e.active = True
        e.hint_setter(True)
        if e.hint_setter:
            e.hint_setter(True)

    def _deactivate(self, ident):
        e = self.__events[ident]
        e.active = False
        if e.hint_setter:
            e.hint_setter(False)

    def activate(self, *idents):
        if isinstance(idents, Iterable):
            for ident in idents:
                self._activate(ident)
        else:
            self._activate(idents)

    def deactivate(self, *idents):
        if isinstance(idents, Iterable):
            for ident in idents:
                self._deactivate(ident)
        else:
            self._deactivate(idents)


@dataclass
class Question:
    index: tuple
    text: str
    answer: str
    category: str
    value: int = -1
    dd: bool = False
    complete: bool = False
    # Medical education extensions
    image_url: str = None          # URL to clinical image (X-ray, CT, path slide, etc.)
    rationale: str = None          # Educational explanation shown after answer
    difficulty: str = None         # "basic", "intermediate", "advanced", "expert"
    specialty: str = None          # Medical specialty (e.g., "Cardiology")
    organ_system: str = None       # Organ system (e.g., "Cardiovascular")
    question_type: str = "standard"  # "standard", "case", "image", "audio"
    references: str = None         # References/sources for the question
    keywords: list = None          # Keywords for categorization/search

    def has_image(self) -> bool:
        """Check if this question has an associated image."""
        return self.image_url is not None and len(self.image_url) > 0

    def has_rationale(self) -> bool:
        """Check if this question has educational rationale."""
        return self.rationale is not None and len(self.rationale) > 0

    def get_timer_type(self) -> str:
        """Get the appropriate timer type for this question."""
        if self.question_type == "case":
            return "complex_case"
        elif self.question_type == "image" or self.has_image():
            return "image_question"
        return "standard_question"


class Board(object):
    size = (6, 5)

    def __init__(self, categories, questions, dj=False):
        self.categories = categories
        self.dj = dj
        if questions is not None:
            self.questions = questions
        else:
            self.questions = []

    def get_question(self, i, j):
        for q in self.questions:
            if q.index == (i, j):
                return q
        return None

    def complete(self):
        return len(self.questions) == 30


class FinalBoard(Board):
    size = (1, 1)

    def __init__(self, category, question):
        super().__init__([category], [question], dj=False)
        self.category = category
        self.question = question

    def complete(self):
        return len(self.questions) == 1


@dataclass
class GameData:
    rounds: list
    date: str
    comments: str


class Game(QObject):
    buzz_trigger = pyqtSignal(int)
    new_player_trigger = pyqtSignal()
    wager_trigger = pyqtSignal(int, int)
    toolate_trigger = pyqtSignal()

    def __init__(self, config: MedJeopardyConfig = None):
        super().__init__()

        # Medical education configuration
        self.config = config or MedJeopardyConfig()

        self.host_display = None
        self.main_display = None
        self.dc = None

        self.data = None

        self.current_round = None
        self.players = []

        self.active_question = None
        self.accepting_responses = False
        self.answering_player = None
        self.previous_answerer = None
        self.timer = None
        self.soliciting_player = False  # part of selecting who found a daily double

        self.song_player = SongPlayer()
        self.__judgement_round = 0
        self.__sorted_players = None

        self.buzzer_controller = None

        self.keystroke_manager = KeystrokeManager()

        # Medical education state
        self.show_rationale_after_answer = self.config.show_rationale
        self.learning_mode = self.config.game_mode == GameMode.LEARNING
        self.cme_tracker = None  # Will be set by main.py if CME tracking is enabled

        self.keystroke_manager.addEvent(
            "CORRECT_ANSWER", Qt.Key.Key_Left, self.correct_answer, self.arrowhints
        )
        self.keystroke_manager.addEvent(
            "INCORRECT_ANSWER", Qt.Key.Key_Right, self.incorrect_answer, self.arrowhints
        )
        self.keystroke_manager.addEvent(
            "BACK_TO_BOARD", Qt.Key.Key_Space, self.back_to_board, self.spacehints
        )
        self.keystroke_manager.addEvent(
            "OPEN_RESPONSES", Qt.Key.Key_Space, self.open_responses, self.spacehints
        )
        self.keystroke_manager.addEvent(
            "NEXT_ROUND", Qt.Key.Key_Space, self.next_round, self.spacehints
        )
        self.keystroke_manager.addEvent(
            "OPEN_FINAL", Qt.Key.Key_Space, self.open_final, self.spacehints
        )
        self.keystroke_manager.addEvent(
            "CLOSE_GAME", Qt.Key.Key_Space, self.close_game, self.spacehints
        )
        self.keystroke_manager.addEvent(
            "FINAL_OPEN_RESPONSES",
            Qt.Key.Key_Space,
            self.final_open_responses,
            self.spacehints,
        )
        self.keystroke_manager.addEvent(
            "FINAL_NEXT_PLAYER",
            Qt.Key.Key_Space,
            self.final_next_player,
            self.spacehints,
        )
        self.keystroke_manager.addEvent(
            "FINAL_SHOW_ANSWER",
            Qt.Key.Key_Space,
            self.final_show_answer,
            self.spacehints,
        )
        self.keystroke_manager.addEvent(
            "FINAL_CORRECT_ANSWER",
            Qt.Key.Key_Left,
            self.final_correct_answer,
            self.arrowhints,
        )
        self.keystroke_manager.addEvent(
            "FINAL_INCORRECT_ANSWER",
            Qt.Key.Key_Right,
            self.final_incorrect_answer,
            self.arrowhints,
        )

        self.wager_trigger.connect(self.wager)
        self.buzz_trigger.connect(self.buzz)
        self.new_player_trigger.connect(self.new_player)
        self.toolate_trigger.connect(self.__toolate)

    def startable(self):
        return self.valid_game() and len(self.buzzer_controller.connected_players) > 0

    def begin_theme_song(self):
        self.song_player.play(repeat=True)

    def start_game(self):
        logging.info("starting game")
        self.current_round = self.data.rounds[0]
        self.dc.show_welcome_widgets(False)
        self.dc.board_widget.load_round(self.current_round)
        self.modify_players(False)
        self.host_display.settings_button.show()
        self.song_player.stop()

    def setDisplays(self, host_display, main_display):
        self.host_display = host_display
        self.main_display = main_display
        self.dc = CompoundObject(host_display, main_display)

    def setBuzzerController(self, controller):
        self.buzzer_controller = controller

    def arrowhints(self, val):
        self.host_display.borders.arrowhints(val)

    def spacehints(self, val):
        self.host_display.borders.spacehints(val)

    def new_player(self):
        new_players = set(self.buzzer_controller.connected_players) - set(self.players)
        self.players = self.buzzer_controller.connected_players

        # Register new players with CME tracker
        if self.cme_tracker:
            for player in new_players:
                self.cme_tracker.record_participant(player)

        self.dc.scoreboard.refresh_players()
        if not self.game_started():
            self.host_display.welcome_widget.check_start()
        if self.is_final():
            self.controller.open_wagers(new_players)



    def remove_player(self, player):
        self.players.remove(player)
        player.waiter.close()
        self.dc.scoreboard.refresh_players()
        self.host_display.welcome_widget.check_start()
        self.check_all_wagered()

    def valid_game(self):
        return self.data is not None and all(b.complete() for b in self.data.rounds)

    def get_question_timer_duration(self, question=None) -> int:
        """Get the appropriate timer duration based on question type and config."""
        q = question or self.active_question
        if q is None:
            return self.config.timers.standard_question

        timer_type = q.get_timer_type()

        if timer_type == "complex_case":
            return self.config.timers.complex_case
        elif timer_type == "image_question":
            return self.config.timers.image_question
        else:
            return self.config.timers.standard_question

    def open_responses(self):
        self.dc.borders.lights(True)
        QApplication.processEvents()
        time.sleep(self.config.timers.buzzer_delay)

        self.accepting_responses = True

        if not self.timer:
            # Use configurable timer based on question type
            duration = self.get_question_timer_duration()
            self.timer = QuestionTimer(duration, self.stumped)

        self.timer.start()

    def modify_players(self, val):
        self.buzzer_controller.accepting_players = val
        self.host_display.scoreboard.show_close_buttons(val)
        self.main_display.show_welcome_widgets(val)
        if val:
            self.main_display.welcome_widget.show()

    def close_responses(self):
        self.timer.pause()
        self.accepting_responses = False
        self.dc.borders.lights(True)

    def buzz(self, i_player):
        player = self.players[i_player]
        if self.accepting_responses and player is not self.previous_answerer:
            logging.info(f"buzz ({time.time():.6f} s)")
            self.accepting_responses = False
            self.timer.pause()
            self.previous_answerer = player
            self.dc.player_widget(player).run_lights()

            self.answering_player = player
            self.keystroke_manager.activate("CORRECT_ANSWER", "INCORRECT_ANSWER")
            self.dc.borders.lights(False)
        elif self.active_question is None:
            self.dc.player_widget(player).buzz_hint()
        else:
            pass

    def answer_given(self):
        self.keystroke_manager.deactivate("CORRECT_ANSWER", "INCORRECT_ANSWER")
        self.dc.player_widget(self.answering_player).stop_lights()
        self.answering_player = None

    def back_to_board(self):
        logging.info("back to board")
        self.dc.hide_question()
        self.timer = None
        self.active_question.complete = True
        self.active_question = None
        self.previous_answerer = None
        if all(q.complete for q in self.current_round.questions):
            logging.info("NEXT ROUND")
            self.keystroke_manager.activate("NEXT_ROUND")

    def index_of_current_round(self):
        return self.data.rounds.index(self.current_round)

    def is_final(self):
        return isinstance(self.current_round, FinalBoard)

    def prev_round(self):
        logging.info("previous round")
        i = self.index_of_current_round()
        logging.info(f"ROUND {i}")
        if i == 0:
            logging.error("Already at first round")

        if self.is_final():
            for player in self.players:
                self.dc.player_widget(player).set_lights(False)
            self.buzzer_controller.close_wagers()
            self.dc.close_final()

        self.current_round = self.data.rounds[i - 1]
        self.dc.board_widget.load_round(self.current_round)


    def next_round(self):
        logging.info("next round")
        i = self.index_of_current_round()
        logging.info(f"ROUND {i}")

        if i == len(self.data.rounds) - 1:
            logging.error("Already at final round")

        self.current_round = self.data.rounds[i + 1]
        if self.is_final():
            self.host_display.set_player_in_control(None)

            self.dc.load_final(self.current_round.question)
            self.start_final()
        else:
            # Highlight player with least money to have control
            losing_player = min(self.players, key=lambda p: p.score)
            self.host_display.set_player_in_control(losing_player)

            self.dc.board_widget.load_round(self.current_round)

    def start_final(self):
        logging.info("start final")
        for player in self.players:
            self.dc.player_widget(player).set_lights(True)

        self.buzzer_controller.open_wagers()

    def wager(self, i_player, amount):
        player = self.players[i_player]
        player.wager = amount
        self.dc.player_widget(player).set_lights(False)
        logging.info(f"{player} wagered {amount}")
        self.check_all_wagered()

    def check_all_wagered(self):
        if all(p.wager is not None for p in self.players) and len(self.players) > 0:
            self.host_display.question_widget.hint_label.setText(
                "Press space to show clue!"
            )
            self.keystroke_manager.activate("OPEN_FINAL")

    def answer(self, player, guess):
        player.finalanswer = guess
        logging.info(f"{player} guessed {guess}")

    def final_open_responses(self):
        self.dc.borders.lights(True)
        self.buzzer_controller.prompt_answers()

        self.song_player.final()

        # Use configurable Final Jeopardy timer
        self.timer = QuestionTimer(self.config.timers.final_jeopardy, self.final_finished_song)
        self.timer.start()

    def final_next_player(self):
        for p in self.players:
            self.dc.player_widget(p).set_lights(False)

        if self.__judgement_round == 0:
            self.dc.load_final_judgement()
            self.__sorted_players = sorted(self.players, key=lambda x: x.score)

        elif self.__judgement_round == len(self.players):
            self.end_game()
            return

        self.answering_player = self.__sorted_players[self.__judgement_round]

        self.dc.player_widget(self.answering_player).set_lights(True)

        self.dc.final_window.guess_label.setText("")
        self.dc.final_window.wager_label.setText("")

        self.keystroke_manager.activate("FINAL_SHOW_ANSWER")

    def final_show_answer(self):
        answer = self.answering_player.finalanswer
        if answer == "":
            answer = "________"

        self.dc.final_window.guess_label.setText(answer)
        self.keystroke_manager.activate(
            "FINAL_CORRECT_ANSWER", "FINAL_INCORRECT_ANSWER"
        )

    def final_correct_answer(self):
        ap = self.answering_player
        self.set_score(ap, ap.score + ap.wager)
        self.final_judgement_given()

    def final_incorrect_answer(self):
        ap = self.answering_player
        self.set_score(ap, ap.score - ap.wager)
        self.final_judgement_given()

    def final_judgement_given(self):
        self.keystroke_manager.deactivate(
            "FINAL_CORRECT_ANSWER", "FINAL_INCORRECT_ANSWER"
        )
        self.dc.final_window.wager_label.setText(str(self.answering_player.wager))
        self.keystroke_manager.activate("FINAL_NEXT_PLAYER")
        self.__judgement_round += 1

    def final_finished_song(self):
        logging.info("Final song ended")
        self.toolate_trigger.emit()
        self.accepting_responses = False
        self.dc.borders.flash()
        self.keystroke_manager.activate("FINAL_NEXT_PLAYER")

    def end_game(self):
        top_score = max([p.score for p in self.players])
        winners = [p for p in self.players if p.score == top_score]
        for w in winners:
            self.dc.player_widget(w).set_lights(True)

        if len(winners) == 1:
            self.dc.final_window.show_winner(winners[0])
        else:
            self.dc.final_window.show_tie()

        print("activate close game")
        self.keystroke_manager.activate("CLOSE_GAME")

    def close_game(self):
        self.buzzer_controller.restart()
        self.players = []
        self.current_round = None
        self.answering_player = None
        self.timer = None
        self.data = None
        self.__judgement_round = 0
        self.modify_players(True)
        self.dc.restart()
        self.begin_theme_song()

    def game_started(self):
        return self.current_round is not None

    def get_dd_wager(self, player):
        self.answering_player = player
        self.soliciting_player = False

        max_wager = max(self.answering_player.score, 1000)
        wager_res = DDWagerDialog.getInt(self.host_display, max_wager)

        if not wager_res[1]:
            self.soliciting_player = True
            return False

        wager = wager_res[0]
        self.active_question.value = wager

        self.keystroke_manager.activate("CORRECT_ANSWER", "INCORRECT_ANSWER")
        self.dc.question_widget.show_question()

    def load_question(self, q):
        self.active_question = q
        if q.dd:
            logging.info("Daily double!")
            wo = sa.WaveObject.from_wave_file(resource_path("dd.wav"))
            wo.play()
            self.soliciting_player = True
        else:
            self.keystroke_manager.activate("OPEN_RESPONSES")
        self.dc.load_question(q)
        self.dc.remove_card(q)

    def open_final(self):
        self.dc.question_widget.show_question()
        self.keystroke_manager.activate("FINAL_OPEN_RESPONSES")

    def correct_answer(self):
        if self.timer:
            self.timer.cancel()

        self.set_score(
            self.answering_player,
            self.answering_player.score + self.active_question.value,
        )
        self.host_display.set_player_in_control(self.answering_player)
        self.dc.borders.lights(False)

        # Record answer for CME tracking
        self.answering_player.record_answer(
            correct=True,
            specialty=self.active_question.specialty
        )
        if self.cme_tracker:
            self.cme_tracker.record_answer(
                self.answering_player,
                self.active_question,
                correct=True
            )

        if self.active_question.dd:
            wo = sa.WaveObject.from_wave_file(resource_path("applause.wav"))
            wo.play()

        self.answer_given()

        # Show rationale in learning mode before returning to board
        if self.show_rationale_after_answer and self.active_question.has_rationale():
            self._show_rationale()
        else:
            self.back_to_board()

    def _show_rationale(self):
        """Show educational rationale after answer in learning mode."""
        if hasattr(self.host_display, 'question_widget') and self.host_display.question_widget:
            self.host_display.question_widget.show_rationale()
        # Activate space to continue after viewing rationale
        self.keystroke_manager.activate("BACK_TO_BOARD")

    def incorrect_answer(self):
        self.set_score(
            self.answering_player,
            self.answering_player.score - self.active_question.value,
        )

        # Record answer for CME tracking
        self.answering_player.record_answer(
            correct=False,
            specialty=self.active_question.specialty
        )
        if self.cme_tracker:
            self.cme_tracker.record_answer(
                self.answering_player,
                self.active_question,
                correct=False
            )

        self.answer_given()
        if self.active_question.dd:
            # Show rationale in learning mode before returning to board
            if self.show_rationale_after_answer and self.active_question.has_rationale():
                self._show_rationale()
            else:
                self.back_to_board()
        else:
            self.open_responses()
            self.timer.resume()

    def stumped(self):
        self.accepting_responses = False
        sa.WaveObject.from_wave_file(resource_path("stumped.wav")).play()
        self.dc.borders.flash()

        # Show rationale in learning mode when no one answers
        if self.show_rationale_after_answer and self.active_question.has_rationale():
            self._show_rationale()
        else:
            self.keystroke_manager.activate("BACK_TO_BOARD")

    def __toolate(self):
        self.buzzer_controller.toolate()

    def set_score(self, player, score):
        player.score = score
        self.dc.player_widget(player).update_score()

    def adjust_score(self, player):
        new_score, answered = QInputDialog.getInt(
            self.host_display,
            "Adjust Score",
            "Enter a new score:",
            value=player.score,
        )
        if answered:
            self.set_score(player, new_score)

    def close(self):
        self.song_player.stop()
        QApplication.quit()


class Team:
    """Team class for team-based medical education sessions."""

    def __init__(self, name: str):
        self.name = name
        self.members = []
        self.score = 0
        self.questions_answered = 0
        self.questions_correct = 0

    def add_member(self, player):
        """Add a player to the team."""
        if player not in self.members:
            self.members.append(player)
            player.team = self.name

    def remove_member(self, player):
        """Remove a player from the team."""
        if player in self.members:
            self.members.remove(player)
            player.team = None

    def total_score(self) -> int:
        """Calculate total team score from all members."""
        return sum(p.score for p in self.members)

    def record_answer(self, correct: bool, specialty: str = None):
        """Record an answer for team statistics."""
        self.questions_answered += 1
        if correct:
            self.questions_correct += 1

    def accuracy(self) -> float:
        """Get team accuracy percentage."""
        if self.questions_answered == 0:
            return 0.0
        return (self.questions_correct / self.questions_answered) * 100


class Player(object):
    def __init__(self, name, waiter):
        self.name = name
        self.token = os.urandom(15)
        self.score = 0
        self.waiter = waiter
        self.wager = None
        self.finalanswer = ""
        self.page = "buzz"
        # Medical education additions
        self.team = None              # Team name if in team mode
        self.team_obj = None          # Reference to Team object
        self.questions_answered = 0   # For CME tracking
        self.questions_correct = 0    # For performance tracking
        self.specialty_scores = {}    # Track scores by specialty

    def __hash__(self):
        return int.from_bytes(self.token, sys.byteorder)

    def state(self):
        return {
            "page": self.page,
            "score": self.score,
            "team": self.team,
            "questions_answered": self.questions_answered,
            "questions_correct": self.questions_correct
        }

    def record_answer(self, correct: bool, specialty: str = None):
        """Record an answer for CME tracking."""
        self.questions_answered += 1
        if correct:
            self.questions_correct += 1
        if specialty:
            if specialty not in self.specialty_scores:
                self.specialty_scores[specialty] = {"correct": 0, "total": 0}
            self.specialty_scores[specialty]["total"] += 1
            if correct:
                self.specialty_scores[specialty]["correct"] += 1

    def accuracy(self) -> float:
        """Get overall accuracy percentage."""
        if self.questions_answered == 0:
            return 0.0
        return (self.questions_correct / self.questions_answered) * 100

    def cme_eligible(self, min_questions: int = 5) -> bool:
        """Check if player meets minimum participation for CME credit."""
        return self.questions_answered >= min_questions
