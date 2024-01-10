#same project program but with classes
#why? OOP improves organization of program

import random
import nltk

nltk.download('words')
from nltk.corpus import words

class ScrabblePractice:
    def __init__(self):
        self.letter_points = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4,
                              'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3,
                              'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8,
                              'y': 4, 'z': 10}

    def main(self):
        print("Welcome to English Scrabble Practice!")
        print("Select a mode:")
        print("1. Practice Mode (Computer generates letters)")
        print("2. Practice Mode (User enters their word)")
        print("3. Practice Mode (User enters highest scoring word)")
        print("4. Quit")

        user_choice = input("Enter the mode number: ")

        if user_choice == '1':
            self.mode_1()
        elif user_choice == '2':
            self.mode_2()
        elif user_choice == '3':
            self.mode_3()
        elif user_choice == '4':
            print("Thanks for playing! Goodbye.")
        else:
            print("Invalid choice. Please try again.")
            self.main()

    def mode_1(self):
        print("Entering Practice Mode 1...")
        while True:
            ready_input = input("Press Enter when ready to generate letters. Enter 'q' to quit: ")

            if ready_input.lower() == 'q':
                print("Exiting Practice Mode 1...")
                break

            letters = self.no_points_generate_letters()
            print("Generated Letters:", ' '.join(letters))

            input("Press Enter to reveal the longest word.")

            word = self.longest_word(letters)
            print("Longest Word:", word)

            user_input = input("Enter 'q' to quit, or press Enter to continue: ")
            if user_input.lower() == 'q':
                print("Exiting Practice Mode 1...")
                break

    def mode_2(self):
        print("Entering Practice Mode 2...")
        while True:
            ready_input = input("Press Enter when ready to generate letters. Enter 'q' to quit: ")

            if ready_input.lower() == 'q':
                print("Exiting Practice Mode 2...")
                break

            letters = self.no_points_generate_letters()
            print("Generated Letters:", ' '.join(letters))

            guess = self.user_input_word(letters)
            correct_word = self.longest_word(letters)

            if len(guess) == len(correct_word) and guess.lower() == correct_word.lower():
                print("Correct! You found the longest word.")
            else:
                print(f"Incorrect. The longest word is: {correct_word}")

            self.reset_tiles()

            user_input_continue = input("Enter 'q' to quit, or press Enter to continue: ")
            if user_input_continue.lower() == 'q':
                print("Exiting Practice Mode 2...")
                break

    def mode_3(self):
        print("Entering Practice Mode 3...")
        while True:
            ready_input = input("Press Enter when ready to generate letters. Enter 'q' to quit: ")

            if ready_input.lower() == 'q':
                print("Exiting Practice Mode 3...")
                break

            letters = self.points_generate_letters()
            print("Generated Letters:", ' '.join(letters))

            guess = self.user_input_word(letters)
            total_score = self.calculate_word_score(guess)

            max_possible_score = self.calculate_word_score(self.longest_word(letters))

            print(f"Score for the word '{guess}': {total_score}")
            print(f"Highest possible score: {max_possible_score}")

            if total_score == max_possible_score:
                print("Congratulations! You found the word with the highest possible score.")

            self.reset_tiles()
            self.show_max_possible_word(letters)

            user_input_continue = input("Enter 'q' to quit, or press Enter to continue: ")
            if user_input_continue.lower() == 'q':
                print("Exiting Practice Mode 3...")
                break

    def show_max_possible_word(self, letters):
        max_word = self.longest_word(letters)
        max_score = self.calculate_word_score(max_word)
        print(f"Word with the highest possible score: '{max_word}' with score {max_score}")

    def reset_tiles(self):
        print("Resetting tiles...")

    def user_input_word(self, letters):
        while True:
            guess = input("Enter your word: ")
            if self.is_valid(guess, letters):
                return guess
            else:
                print("Invalid word. Use only the provided letters.")

    def is_valid(self, word, available_letters):
        for letter in word:
            if word.count(letter) > available_letters.count(letter):
                return False
        return True

    def no_points_generate_letters(self, amount=7):
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        return random.sample(alphabet, amount)

    def longest_word(self, letters):
        english_word_list = set(words.words())
        valid_words = [word for word in english_word_list if self.is_valid(word, letters)]

        if valid_words:
            return max(valid_words, key=len)
        else:
            return "No valid word found."

    def points_generate_letters(self, amount=7):
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        weighted_alphabet = ''.join(char * weight for char, weight in self.letter_points.items())
        return random.sample(weighted_alphabet, min(amount, len(weighted_alphabet)))

    def calculate_word_score(self, word):
        return sum(self.letter_points[char] for char in word.lower())

if __name__ == "__main__":
    ScrabblePractice().main()
