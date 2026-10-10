import json, os, sys

from pathlib import Path

from flashcard import Flashcard
from deck import Deck
from deck_manager import DeckManager

# Create a Path variable by getting the current file (__file__)'s parent, then navigate to cards.json through data
# DATA_FILE = Path(__file__).resolve().parent / "data" / "cards.json"

if getattr(sys, "frozen", False):
    DATA_DIR = Path(
        os.environ.get("LOCALAPPDATA", str(Path.home()))
    ) / "Flashcards"
else:
    DATA_DIR = Path(__file__).resolve().parent / "data"

DATA_FILE = DATA_DIR / "cards.json"


def load_decks():
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not DATA_FILE.exists():
        deck_manager = DeckManager({})
        save_decks(deck_manager)
        return deck_manager

    with DATA_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    decks = {}

    for deck_name, card_data in data.items():
        flashcards = []

        for card in card_data:
            flashcards.append(
                Flashcard(
                    card["question"],
                    card["answer"],
                    card.get("correct")
                )
            )

        decks[deck_name] = Deck(flashcards)

    return DeckManager(decks)

def save_decks(deck_manager):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    data = {}

    for deck_name, deck in deck_manager.decks.items():
        cards = []

        for flashcard in deck.flashcards:
            cards.append({
                "question" : flashcard.question,
                "answer" : flashcard.answer,
                "correct" : flashcard.correct
            })

        data[deck_name] = cards

    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)