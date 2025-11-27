from PyQt6.QtGui import (
    QPainter,
    QPen,
    QColor,
    QFont,
    QPixmap,
)
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import logging

from jparty.style import MyLabel, CARDPAL


class QuestionWidget(QWidget):
    def __init__(self, question, parent=None):
        super().__init__(parent)
        self.question = question
        self.setAutoFillBackground(True)

        self.main_layout = QVBoxLayout()

        # Image support for medical questions
        self.image_label = None
        if question.has_image():
            self._setup_image_display()

        self.question_label = MyLabel(question.text.upper(), self.startFontSize, self)
        self.question_label.setFont(QFont("ITC_ Korinna"))
        self.main_layout.addWidget(self.question_label)

        # Difficulty indicator for medical questions
        if question.difficulty:
            self._add_difficulty_indicator()

        self.setLayout(self.main_layout)
        self.setPalette(CARDPAL)
        self.show()

    def _setup_image_display(self):
        """Setup image display for clinical images."""
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumHeight(200)
        self.main_layout.addWidget(self.image_label, stretch=3)

        # Load image from URL
        self._load_image(self.question.image_url)

    def _load_image(self, url):
        """Load image from URL asynchronously."""
        try:
            self.network_manager = QNetworkAccessManager(self)
            self.network_manager.finished.connect(self._on_image_loaded)
            request = QNetworkRequest(QUrl(url))
            self.network_manager.get(request)
        except Exception as e:
            logging.error(f"Failed to load image: {e}")
            if self.image_label:
                self.image_label.setText("[Image unavailable]")

    def _on_image_loaded(self, reply: QNetworkReply):
        """Handle loaded image."""
        if reply.error() == QNetworkReply.NetworkError.NoError:
            data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            if not pixmap.isNull() and self.image_label:
                # Scale image to fit while maintaining aspect ratio
                scaled = pixmap.scaled(
                    self.width() - 40,
                    int(self.height() * 0.4),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.image_label.setPixmap(scaled)
        else:
            logging.error(f"Image load error: {reply.errorString()}")
            if self.image_label:
                self.image_label.setText("[Image unavailable]")
        reply.deleteLater()

    def _add_difficulty_indicator(self):
        """Add difficulty indicator for medical questions."""
        difficulty_colors = {
            "basic": "#4CAF50",        # Green
            "intermediate": "#FFC107",  # Yellow
            "advanced": "#FF9800",      # Orange
            "expert": "#F44336"         # Red
        }
        color = difficulty_colors.get(self.question.difficulty.lower(), "#9E9E9E")
        indicator = QLabel(f"[{self.question.difficulty.upper()}]", self)
        indicator.setStyleSheet(f"color: {color}; font-size: 14px; font-weight: bold;")
        indicator.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.main_layout.addWidget(indicator)

    def startFontSize(self):
        return self.width() * 0.05


class HostQuestionWidget(QuestionWidget):
    def __init__(self, question, parent=None):
        super().__init__(question, parent)

        self.question_label.setText(question.text)
        self.main_layout.setStretchFactor(self.question_label, 6)
        self.main_layout.addSpacing(self.main_layout.contentsMargins().top())
        self.answer_label = MyLabel(question.answer, self.startFontSize, self)
        self.answer_label.setFont(QFont("ITC_ Korinna"))
        self.main_layout.addWidget(self.answer_label, 1)

        # Rationale display for medical education mode
        self.rationale_label = None
        self.rationale_visible = False
        if question.has_rationale():
            self._setup_rationale_display()

        # Specialty/system tags for medical questions
        if question.specialty or question.organ_system:
            self._add_medical_tags()

    def _setup_rationale_display(self):
        """Setup rationale display for educational mode."""
        self.rationale_label = MyLabel(
            f"<b>Rationale:</b> {self.question.rationale}",
            lambda: self.startFontSize() * 0.7,
            self
        )
        self.rationale_label.setStyleSheet("color: #90CAF9; padding: 10px;")
        self.rationale_label.setWordWrap(True)
        self.rationale_label.setVisible(False)
        self.main_layout.addWidget(self.rationale_label)

    def _add_medical_tags(self):
        """Add specialty and organ system tags."""
        tags = []
        if self.question.specialty:
            tags.append(f"<span style='color: #81C784;'>{self.question.specialty}</span>")
        if self.question.organ_system:
            tags.append(f"<span style='color: #FFB74D;'>{self.question.organ_system}</span>")

        tag_label = QLabel(" | ".join(tags), self)
        tag_label.setStyleSheet("font-size: 12px;")
        tag_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.main_layout.addWidget(tag_label)

    def show_rationale(self):
        """Show the educational rationale."""
        if self.rationale_label and not self.rationale_visible:
            self.rationale_label.setVisible(True)
            self.rationale_visible = True

    def hide_rationale(self):
        """Hide the educational rationale."""
        if self.rationale_label:
            self.rationale_label.setVisible(False)
            self.rationale_visible = False

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QPen(QColor("white")))
        # Find the index of the answer label in the layout
        for i in range(self.main_layout.count()):
            item = self.main_layout.itemAt(i)
            if item and item.widget() == self.answer_label:
                line_y = item.geometry().top()
                qp.drawLine(0, line_y, self.width(), line_y)
                break


class DailyDoubleWidget(QuestionWidget):
    def __init__(self, question, parent=None):
        super().__init__(question, parent)
        self.question_label.setVisible(False)

        self.dd_label = MyLabel("DAILY<br/>DOUBLE!", self.startDDFontSize, self)
        self.main_layout.replaceWidget(self.question_label, self.dd_label)

    def startDDFontSize(self):
        return self.width() * 0.2

    def show_question(self):
        self.main_layout.replaceWidget(self.dd_label, self.question_label)
        self.dd_label.deleteLater()
        self.dd_label = None
        self.question_label.setVisible(True)


class HostDailyDoubleWidget(HostQuestionWidget, DailyDoubleWidget):
    def __init__(self, question, parent=None):
        super().__init__(question, parent)
        self.answer_label.setVisible(False)

        self.main_layout.setStretchFactor(self.dd_label, 6)
        self.hint_label = MyLabel(
            "Click the player below who found the Daily Double",
            self.startFontSize,
            self,
        )
        self.main_layout.replaceWidget(self.answer_label, self.hint_label)
        self.main_layout.setStretchFactor(self.hint_label, 1)

    def show_question(self):
        super().show_question()
        self.main_layout.replaceWidget(self.hint_label, self.answer_label)
        self.hint_label.deleteLater()
        self.hint_label = None
        self.answer_label.setVisible(True)


class FinalJeopardyWidget(QuestionWidget):
    def __init__(self, question, parent=None):
        super().__init__(question, parent)
        self.question_label.setVisible(False)

        self.category_label = MyLabel(
            question.category, self.startCategoryFontSize, self
        )
        self.main_layout.replaceWidget(self.question_label, self.category_label)

    def startCategoryFontSize(self):
        return self.width() * 0.1

    def show_question(self):
        self.main_layout.replaceWidget(self.category_label, self.question_label)
        self.category_label.deleteLater()
        self.category_label = None
        self.question_label.setVisible(True)


class HostFinalJeopardyWidget(FinalJeopardyWidget, HostQuestionWidget):
    def __init__(self, question, parent):
        self.display = parent
        super().__init__(question, parent)
        self.answer_label.setVisible(False)

        self.main_layout.setStretchFactor(self.question_label, 6)
        self.hint_label = MyLabel(
            "Waiting for all players to wager...", self.startFontSize, self
        )
        self.main_layout.replaceWidget(self.answer_label, self.hint_label)
        self.main_layout.setStretchFactor(self.hint_label, 1)

    def hide_hint(self):
        self.hint_label.setVisible(True)

    def show_question(self):
        super().show_question()
        self.main_layout.replaceWidget(self.hint_label, self.answer_label)
        self.display.settings_button.setVisible(False)
        self.hint_label.deleteLater()
        self.hint_label = None
        self.answer_label.setVisible(True)
