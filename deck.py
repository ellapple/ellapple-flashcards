class Deck:
    def __init__(self, flashcards):
        self.flashcards = flashcards
        self.current_card = 0

    def current(self):
        return self.flashcards[self.current_card]

    def next(self):
        if self.current_card < len(self.flashcards) - 1:
            self.current_card += 1
    
    def previous(self):
        if self.current_card > 0:
            self.current_card -= 1
    
    def count(self):
        return len(self.flashcards)

    def position(self):
        return self.current_card + 1

    def add(self, flashcard):
        self.flashcards.append(flashcard)

    def remove(self, index):
        if not 0 <= index < len(self.flashcards):
            return
        
        self.flashcards.pop(index)

        if not self.flashcards:
            self.current_card = 0
        elif self.current_card > index:
            self.current_card -= 1
        elif self.current_card >= len(self.flashcards):
            self.current_card = len(self.flashcards) - 1 # Would also work with -= 1, but I suppose this is more readable