import time
import pyautogui
from threading import Timer


class Game:
    def __init__(self):
        self.name = input("Enter your name: ")
        self.goal = 100
        self.time_limit = 3

    def reset(self):
        self.curr_number = 2
        self.player_input = None
        self.computer_input = None
        self.time_is_up = False

    def computer_move(self):
        if self.curr_number % 3 == 0 and self.curr_number % 5 == 0:
            self.computer_input = "Fizz Buzz"
        elif self.curr_number % 3 == 0:
            self.computer_input = "Fizz"
        elif self.curr_number % 5 == 0:
            self.computer_input = "Buzz"
        else:
            self.computer_input = str(self.curr_number)

    def times_up(self):
        self.time_is_up = True
        print("\nToo slow!")
        pyautogui.press("enter")

    def wrong_answer(self):
        print("\nWrong!")
        self.game_over()

    def game_over(self):
        self.save_score()
        self.show_scores()

        if input("\nPlay again? Y/N: ").lower() == "y":
            self.reset()
            self.play_game()
        else:
            exit()

    def player_move(self):
        timer = Timer(self.time_limit, self.times_up)
        timer.start()

        self.player_input = input("Your move: ")

        timer.cancel()

    def save_score(self):
        with open("data/scores.txt", "a+") as score_file:
            score_file.write(f"{self.name}:{self.curr_number}\n")
    
    def show_scores(self):
        scores = {}

        with open("data/scores.txt", "r") as score_file:
            for line in score_file:
                name, score = line.split(":")
                scores[name] = int(score)
        
        scores = ((val, key) for (key, val) in scores.items())
        scores = reversed(sorted(scores))
        
        scores_sorted = {}

        for item in scores:
            scores_sorted[item[1]] = int(item[0])

        print(f"\n    ...HIGH SCORES:...\n")
        
        count = 1

        for item in scores_sorted:
            if count <= 10:
                person = item
                score = scores_sorted[person]
                print(f"{count}. {person.replace(' ','').upper()[:7]}\t\t{score}")
                count += 1

    def play_game(self):
        self.reset()
        print("\nComputer move: 1")

        while 0 < self.curr_number <= self.goal:
            self.player_move()

            if self.time_is_up:
                break

            self.computer_move()

            if self.player_input.title() != self.computer_input:
                print("Wrong!")
                break

            if self.curr_number == self.goal:
                print("\nCongratulations! You've won.")
                break

            self.curr_number += 1

            self.computer_move()
            time.sleep(1)
            print(f"Computer move: {self.computer_input}")

            self.curr_number += 1

        self.game_over()

a = Game()
a.play_game()

# Format printing of high scores with dots;
# Write intro;
# Fix issue where when you loose, one extra point is added to your score.