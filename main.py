import sys

from PySide6.QtWidgets import (
    QApplication, 
    QWidget, 
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QSizePolicy,
    QDialog,
    QMessageBox,
    QLineEdit,
    QDialogButtonBox,
    QFormLayout,
    QInputDialog
)

from PySide6.QtGui import QKeySequence, QShortcut, QFont

from PySide6.QtCore import Qt

from flashcard import Flashcard
from deck import Deck
from data_manager import load_decks, save_decks

class FlashcardDialog(QDialog):
    def __init__(self, question = "", answer = "", parent = None, editing = False):
        super().__init__(parent)

        self.setWindowTitle("Edit Flashcard" if editing else "New Flashcard")
        self.setMinimumWidth(360)

        self.question_input = QLineEdit(question)
        self.answer_input = QLineEdit(answer)

        self.question_input.setPlaceholderText("Enter question here")
        self.answer_input.setPlaceholderText("Enter answer here")

        form_layout = QFormLayout()
        form_layout.addRow("Question:", self.question_input)
        form_layout.addRow("Answer:", self.answer_input)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        dialog_layout = QVBoxLayout()
        dialog_layout.addLayout(form_layout)
        dialog_layout.addWidget(self.buttons)

        self.setLayout(dialog_layout)

    def get_values(self):
        return (
            self.question_input.text().strip(),
            self.answer_input.text().strip()
        )

# -------------------------------------------------------------------------------------------------
# Load decks and choose initial deck
# -------------------------------------------------------------------------------------------------

deck_manager = load_decks()
deck_names = deck_manager.names()

if "Biology" in deck_names:
    initial_deck_name = "Biology"
elif deck_names:
    initial_deck_name = deck_names[0]
else:
    initial_deck_name = None

deck = (
    deck_manager.get(initial_deck_name)
    if initial_deck_name is not None
    else None
)

# -------------------------------------------------------------------------------------------------
# Application and window setup
# -------------------------------------------------------------------------------------------------

app = QApplication(sys.argv)

window = QWidget()

window.setStyleSheet("""
    QWidget {
        background-color: #5f5f7f;
        color: white;
        font-family: "Segoe UI";
    }

    QPushButton {
        border: none;
        border-radius: 12px;
        padding: 8px;
        font-size: 16px;
        font-weight: 500;
    }

    QPushButton#navigationButton {
        background-color: white;
        color: #222222;
    }

    QPushButton#navigationButton:hover {
        background-color: #eeeeee;
    }

    QPushButton#navigationButton:disabled {
        background-color: #dfdfdf;
    }

    QPushButton#resultButton {
        background-color: #e8e8f0;
        color: #222222;
    }

    QPushButton#resultButton:hover {
        background-color: white;
    }

    QPushButton#flashcard {
        background-color: white;
        color: #222222;
        border-radius: 24px;
        padding: 36px;
        font-size: 24px;
        font-weight: 500;
    }

    QPushButton#flashcard:hover {
        background-color: #fafafa;
    }

    QPushButton#flashcard:pressed {
        background-color: #eeeeee;
    }

    QPushButton:disabled {
        color: #999999;
        background-color: #dddddd;
    }
""")

window.setWindowTitle("Flashcards")
window.resize(800, 600)
window.setMinimumSize(400, 600)

# -------------------------------------------------------------------------------------------------
# Main layout and title
# -------------------------------------------------------------------------------------------------

layout = QVBoxLayout()
layout.setContentsMargins(40, 30, 40, 30)
layout.setSpacing(16)

title = QLabel("Flashcards")
title.setAlignment(Qt.AlignmentFlag.AlignCenter)
title.setStyleSheet("""
    color: white;
    font-size: 32px;
    font-weight: 600;
""")

layout.addWidget(title)

# -------------------------------------------------------------------------------------------------
# Deck selector
# -------------------------------------------------------------------------------------------------

deck_selector = QComboBox()

combo_font = QFont("Segoe UI", 12)

deck_selector.setFont(combo_font)
deck_selector.view().setFont(combo_font)

deck_selector.setStyleSheet("""
    QComboBox {
        background-color: white;
        border: none;
        border-radius: 12px;
        color: black;
        padding: 12px 16px;
    }

    QComboBox:hover {
        background-color: #f5f5f5;
    }

    QComboBox QAbstractItemView {
        background-color: white;
        color: #222222;
        selection-background-color: #e5e5ea;
        selection-color: #222222;
        outline: none;
    }
""")

deck_selector.addItems(deck_names)

if initial_deck_name is not None:
    deck_selector.setCurrentText(initial_deck_name)

layout.addWidget(deck_selector)

# -------------------------------------------------------------------------------------------------
# Deck management
# -------------------------------------------------------------------------------------------------

deck_management_layout = QHBoxLayout()

add_deck_button = QPushButton("Add Deck")
rename_deck_button = QPushButton("Edit Deck Name")
delete_deck_button = QPushButton("Delete Deck")

add_deck_button.setObjectName("resultButton")
rename_deck_button.setObjectName("resultButton")
delete_deck_button.setObjectName("resultButton")

deck_management_layout.addWidget(add_deck_button)
deck_management_layout.addWidget(rename_deck_button)
deck_management_layout.addWidget(delete_deck_button)

layout.addLayout(deck_management_layout)

# -------------------------------------------------------------------------------------------------
# Flashcard display and progress indicator
# -------------------------------------------------------------------------------------------------

showing_answer = False

card = QPushButton()
card.setMinimumHeight(220)
card.setSizePolicy(
    QSizePolicy.Policy.Expanding,
    QSizePolicy.Policy.Expanding
)

card.setObjectName('flashcard')

layout.addWidget(card)

progress_label = QLabel()
progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
progress_label.setStyleSheet("""
    background-color: transparent;
    color: #eeeef5;
    font-size: 12px;
""")

layout.addWidget(progress_label)

# -------------------------------------------------------------------------------------------------
# Navigation buttons
# -------------------------------------------------------------------------------------------------

navigation_layout = QHBoxLayout()

previous_button = QPushButton("Previous")
next_button = QPushButton("Next")

previous_button.setObjectName('navigationButton')
next_button.setObjectName('navigationButton')

navigation_layout.addWidget(previous_button)
navigation_layout.addWidget(next_button)

layout.addLayout(navigation_layout)

# -------------------------------------------------------------------------------------------------
# Correct and incorrect buttons
# -------------------------------------------------------------------------------------------------

result_layout = QHBoxLayout()

incorrect_button = QPushButton("Incorrect")
correct_button = QPushButton("Correct")

incorrect_button.setObjectName('resultButton')
correct_button.setObjectName('resultButton')

result_layout.addWidget(incorrect_button)
result_layout.addWidget(correct_button)

layout.addLayout(result_layout)

# -------------------------------------------------------------------------------------------------
# Flashcard management
# -------------------------------------------------------------------------------------------------

card_management_layout = QHBoxLayout()

add_card_button = QPushButton("Add")
edit_card_button = QPushButton("Edit")
delete_card_button = QPushButton("Delete")

add_card_button.setObjectName('resultButton')
edit_card_button.setObjectName('resultButton')
delete_card_button.setObjectName('resultButton')

card_management_layout.addWidget(add_card_button)
card_management_layout.addWidget(edit_card_button)
card_management_layout.addWidget(delete_card_button)

layout.addLayout(card_management_layout)

# -------------------------------------------------------------------------------------------------
# Flashcard Functions
# -------------------------------------------------------------------------------------------------

def update_card():
    global showing_answer

    if deck is None or deck.count() == 0:
        card.setText("This deck is empty!")
        card.setEnabled(False)
        progress_label.setText("0 / 0")

        previous_button.setEnabled(False)
        next_button.setEnabled(False)
        incorrect_button.setEnabled(False)
        correct_button.setEnabled(False)

        add_card_button.setEnabled(deck is not None)
        edit_card_button.setEnabled(False)
        delete_card_button.setEnabled(False)

        showing_answer = False

        return

    flashcard = deck.current()

    card.setEnabled(True)
    card.setText(flashcard.question)
    showing_answer = False

    previous_button.setEnabled(deck.position() > 1)
    next_button.setEnabled(deck.position() < deck.count())
    incorrect_button.setEnabled(True)
    correct_button.setEnabled(True)

    add_card_button.setEnabled(True)
    edit_card_button.setEnabled(True)
    delete_card_button.setEnabled(True)

    if flashcard.correct is True:
        result = " · Correct"
    elif flashcard.correct is False:
        result = " · Incorrect"
    else:
        result = ""

    progress_label.setText(
        f"{deck.position()} / {deck.count()}{result}"
    )

def flip_card():
    if deck is None or deck.count() == 0:
        return

    global showing_answer

    flashcard = deck.current()

    if showing_answer:
        card.setText(flashcard.question)
        showing_answer = False
    else:
        card.setText(flashcard.answer)
        showing_answer = True

def previous_card():
    if deck is None or deck.count() == 0:
        return

    deck.previous()
    update_card()

def next_card():
    if deck is None or deck.count() == 0:
        return

    deck.next()
    update_card()

def mark_correct():
    if deck is None or deck.count() == 0:
        return
    
    deck.current().mark_correct()
    save_decks(deck_manager)
    update_card()

def mark_incorrect():
    if deck is None or deck.count() == 0:
        return

    deck.current().mark_incorrect()
    save_decks(deck_manager)
    update_card()

def change_deck(index):
    global deck

    if index < 0:
        deck = None
    else:
        deck_name = deck_selector.itemText(index)
        deck = deck_manager.get(deck_name)

    update_card()

def add_deck():
    name, accepted = QInputDialog.getText(
        window,
        "Add Deck",
        "Enter deck name here: "
    )

    if not accepted:
        return

    name = name.strip()

    if not name:
        QMessageBox.warning(
            window,
            "Invalid Name",
            "The deck name cannot be empty"
        )
        return

    if not deck_manager.add(name, Deck([])):
        QMessageBox.warning(
            window,
            "Duplicate Name",
            "A deck with that name already exists"
        )
        return

    deck_selector.addItem(name)
    deck_selector.setCurrentText(name)
    save_decks(deck_manager)
    update_card()

def rename_deck():
    global deck

    if deck is None:
        return
    
    old_name = deck_selector.currentText()

    new_name, accepted = QInputDialog.getText(
        window,
        "Rename Deck",
        "Enter new deck name here: ",
        text=old_name
    )

    if not accepted:
        return

    new_name = new_name.strip()

    if not new_name:
        QMessageBox.warning(
            window,
            "Invalid Name",
            "The deck name cannot be empty"
        )
        return

    if not deck_manager.rename(old_name, new_name):
        QMessageBox.warning(
            window,
            "Duplicate Name",
            "A deck with that name already exists"
        )
        return

    index = deck_selector.currentIndex()
    deck_selector.setItemText(index, new_name)

    deck = deck_manager.get(new_name)

    save_decks(deck_manager)
    
def delete_deck():
    if deck is None:
        return

    name = deck_selector.currentText()

    confirmation = QMessageBox.question(
        window,
        "Delete Deck",
        f"Are you sure you want to delete '{name}' and all its flashcards?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No
    )

    if confirmation != QMessageBox.StandardButton.Yes:
        return

    if not deck_manager.remove(name):
        return

    index = deck_selector.currentIndex()

    deck_selector.removeItem(index)
    if deck_selector.count() > 0:
        deck_selector.setCurrentIndex(min(index, deck_selector.count() - 1))
    else:
        change_deck(-1)

    save_decks(deck_manager)
    update_card()

def add_flashcard():
    if deck is None:
        return

    dialog = FlashcardDialog(parent=window)

    if dialog.exec() != QDialog.DialogCode.Accepted:
        return

    question, answer = dialog.get_values()

    if not question or not answer:
        QMessageBox.warning(
            window,
            "Invalid flashcard",
            "Both the question and answer are required."
        )
        return

    deck.add(Flashcard(question, answer))

    save_decks(deck_manager)
    update_card()

def edit_flashcard():
    if deck is None:
        return

    flashcard = deck.current()

    dialog = FlashcardDialog(
        question=flashcard.question,
        answer=flashcard.answer,
        parent=window,
        editing=False
    )

    if dialog.exec() != QDialog.DialogCode.Accepted:
        return

    question, answer = dialog.get_values()

    if not question or not answer:
        QMessageBox.warning(
            window,
            "Invalid flashcard",
            "Both the question and answer are required."
        )
        return

    flashcard.question = question
    flashcard.answer = answer
    flashcard.correct = None

    save_decks(deck_manager)
    update_card()

def delete_flashcard():
    if deck is None or deck.count() == 0:
        return

    confirmation = QMessageBox.question(
        window,
        "Delete Flashcard",
        "Are you sure you want to delete this flashcard?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No
    )

    if confirmation != QMessageBox.StandardButton.Yes:
        return

    deck.remove(deck.current_card)

    save_decks(deck_manager)
    update_card()

# -------------------------------------------------------------------------------------------------
# Connect buttons and deck selector
# -------------------------------------------------------------------------------------------------

card.clicked.connect(flip_card)

previous_button.clicked.connect(previous_card)
next_button.clicked.connect(next_card)

incorrect_button.clicked.connect(mark_incorrect)
correct_button.clicked.connect(mark_correct)

add_card_button.clicked.connect(add_flashcard)
edit_card_button.clicked.connect(edit_flashcard)
delete_card_button.clicked.connect(delete_flashcard)

add_deck_button.clicked.connect(add_deck)
rename_deck_button.clicked.connect(rename_deck)
delete_deck_button.clicked.connect(delete_deck)

deck_selector.currentIndexChanged.connect(change_deck)

# -------------------------------------------------------------------------------------------------
# Keyboard shortcuts
# -------------------------------------------------------------------------------------------------

previous_shortcut = QShortcut(QKeySequence("Left"), window)
previous_shortcut.activated.connect(previous_card)

next_shortcut = QShortcut(QKeySequence("Right"), window)
next_shortcut.activated.connect(next_card)

incorrect_shortcut = QShortcut(QKeySequence("Down"), window)
incorrect_shortcut.activated.connect(mark_incorrect)

correct_shortcut = QShortcut(QKeySequence("Up"), window)
correct_shortcut.activated.connect(mark_correct)

flip_shortcut = QShortcut(QKeySequence("Space"), window)
flip_shortcut.activated.connect(flip_card)

# -------------------------------------------------------------------------------------------------
# Start application
# -------------------------------------------------------------------------------------------------

update_card()

window.setLayout(layout)

window.show()

app.aboutToQuit.connect(lambda: save_decks(deck_manager))

sys.exit(app.exec())