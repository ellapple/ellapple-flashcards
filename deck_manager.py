class DeckManager:
    def __init__(self, decks):
        self.decks = decks
        self.current_deck = None

    def add(self, name, deck):
        if name in self.decks:
            return False

        self.decks[name] = deck
        return True

    def get(self, name):
        return self.decks[name]

    def names(self):
        return list(self.decks.keys())

    def rename(self, old_name, new_name):
        if new_name in self.decks and new_name != old_name:
            return False

        self.decks[new_name] = self.decks.pop(old_name)
        return True

    def remove(self, name):
        if name not in self.decks:
            return False

        del self.decks[name]
        return True