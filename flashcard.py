class Flashcard:
    def __init__(self, question, answer, correct = None):
        self.question = question
        self.answer = answer
        self.correct = correct

    def mark_correct(self):
        self.correct = True

    def mark_incorrect(self):
        self.correct = False