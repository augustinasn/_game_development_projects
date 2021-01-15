#Import prerequisites:

from random import randint
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import csv


# Initialize functions and classes:

class Game:
    def __init__(self):
        self.score = 0
        self.lives = 5
        self.secret_word = ""
        self.hint = ""
        self.display_seq = []
        self.used_guesses = []
        self.word_is_ready = True

    def load_word(self):
        words = {}

        try:
            input_file = csv.reader(open("data/words/words.txt"))
        except:
            print("\nFile \"words.txt\" is not found. Unable to load a word list.")
            self.word_is_ready = False
        else:
            for row in input_file:
                if row:
                    k, v = row
                    words[k] = v
                else:
                    pass

            self.secret_word = list(words.keys())[randint(1, len(words)) - 1]
            self.hint = words[self.secret_word].lstrip().capitalize()
            self.display_seq = list(map(lambda x : "_", list(self.secret_word)))

    def show_hangman(self):
        img = mpimg.imread(f"data/pics/{5 - self.lives}.png")
        imgplot = plt.imshow(img)
        plt.show()

    def show_dashes(self):
        print(" ".join(self.display_seq))

    def guess(self, input_letter):
        if input_letter.lower() in list(self.secret_word.lower()):
            self.used_guesses.append(input_letter)

            for i in range(len(self.secret_word)):
                if list(self.secret_word)[i] == guess:
                    self.display_seq[i] = guess

        else:
            self.lives = self.lives - 1
            print("\nLetter", input_letter, "is not present in the word.")
            self.used_guesses.append(input_letter)

new_game = Game()

new_game.load_word()
print(new_game.score)
print(new_game.lives)
print(new_game.secret_word)
print(new_game.hint)
new_game.show_hangman()
new_game.show_dashes()

new_game.guess("a")
new_game.show_dashes()
new_game.show_hangman()

# Runtime:

#while new_game.word_is_ready:





