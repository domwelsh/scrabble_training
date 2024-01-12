import random
import twl

class Tile:
    def __init__(self, letter, tile_count, points_value):
        self.letter = letter
        self.tile_count = tile_count
        self.points = points_value
        self.max_tile_count = tile_count
        self.reset_tiles()

    def __str__(self):
        return f"Tile {self.letter}: {self.tile_count} remaining, {self.points} points per tile"

    def tiles_withdrawn(self):
        if self.tile_count > 0:
            self.tile_count -= 1

    def is_empty(self):
        return self.tile_count == 0

    def reset_tiles(self):
        self.tile_count = self.max_tile_count

def main():
    print("Welcome to English Scrabble Practice!")
    user_choice = None

    while True:
        if user_choice == None:
            pass
        elif user_choice == '1':
            mode_1()
        elif user_choice == '2':
            mode_2()
        elif user_choice == '3':
            mode_3()
        elif user_choice == 'q':
            print("Thanks for playing! Goodbye.")
            break
        else:
            print("Invalid choice. Please try again.")
        print("Select a mode:")
        print("1. Show all longest words")
        print("2. Enter your longest word guesses")
        print("3. Practice Mode (User enters highest scoring word)")
        print("q. Quit")
        user_choice = input("Enter the mode number: ")

def mode_1():
    print("Entering Practice Mode 1...")
    while True:
        if ready_input() == 'q':
            break

        letters = no_points_generate_letters()
        print("Generated Letters:", ' '.join(letters))
        
        input("Press Enter to reveal the longest words.")
        
        words = longest_words(letters)
        if isinstance(words, str):
            print(words)
        elif len(words) == 1:
            print("Longest Word:", words[0])
        else:
            print("Longest Words:")
            for w in words:
                print(w)

def mode_2():
    print("Entering Practice Mode 2...")
    while True:
        if ready_input() == 'q':
            break

        letters = no_points_generate_letters()
        print("Generated Letters:", ' '.join(letters))
        
        guess = user_input_word(letters)
        correct_words = longest_words(letters)

        if isinstance(correct_words, str) and guess == "":
            print(f"Correct. {correct_words}")
        elif isinstance(correct_words, str) and guess != "":
            print(f"Incorrect. {correct_words}")
        elif len(guess) == len(correct_words) and guess.lower() == correct_words.lower():
            if len(correct_words) == 1:
                print("Correct! You found the longest word.")
            else:
                print("Correct! You found one of the longest words. The other longest words are:")
                for w in correct_words:
                    print(w)
        else:
            if len(correct_words) == 1:
                print(f"Incorrect. The longest word is: {correct_words[0]}")
            else:
                print(f"Incorrect. The longest words are:")
                for w in correct_words:
                    print(w)

def mode_3():
    print("Entering Practice Mode 3...")

    # Create instances of Tile based on the data
    tiles_to_generate = [
        ('a', 9, 1),
        ('b', 2, 3),
        ('c', 2, 3),
        ('d', 4, 2),
        ('e', 12, 1),
        ('f', 2, 4),
        ('g', 3, 2),
        ('h', 2, 4),
        ('i', 9, 1),
        ('j', 1, 8),
        ('k', 1, 5),
        ('l', 4, 1),
        ('m', 2, 3),
        ('n', 6, 1),
        ('o', 8, 1),
        ('p', 2, 3),
        ('q', 1, 10),
        ('r', 6, 1),
        ('s', 4, 1),
        ('t', 6, 1),
        ('u', 4, 1),
        ('v', 2, 4),
        ('w', 2, 4),
        ('x', 1, 8),
        ('y', 2, 4),
        ('z', 1, 10),
        ('?', 2, 0)
    ]

    tile_instances = [Tile(letter, count, points) for letter, count, points in tiles_to_generate]

    while True:
        ready_input = input("Press Enter when ready to generate letters. Enter 'q' to quit: ")

        if ready_input.lower() == 'q':
            print("Exiting Practice Mode 3...")
            break

        # Generate letters using Tile instances
        letters_points = points_generate_letters(tile_instances)
        print("Generated Letters:", ' '.join(letter for letter, _ in letters_points))

        # Get user's word guess
        guess = user_input_word(letters_points)

        # Calculate total score for the user's guess
        total_score = calculate_word_score(guess, tile_instances)
        print(f"Score for the word '{guess}': {total_score}")

        # Get the highest scoring word
        highest_scoring_word, highest_score = highest_point_word(tile_instances)
        print(f"Highest scoring word: '{highest_scoring_word}' with score: {highest_score}")

        # Compare user's score with the highest score
        compare_score(highest_score, total_score)

        # Option to reset tiles
        reset_option = input("Do you want to reset the tiles? (y/n): ")
        if reset_option.lower() == 'y':
            reset_tiles(tile_instances)

        # Option to continue or quit
        user_input_continue = input("Enter 'q' to quit, or press Enter to continue: ")
        if user_input_continue.lower() == 'q':
            print("Exiting Practice Mode 3...")
            break

def points_generate_letters(tile_instances, amount=7):
    available_letters = [(tile.letter, tile.points) for tile in tile_instances if not tile.is_empty()]
    selected_letters = random.sample(available_letters, min(amount, len(available_letters)))

    # Withdraw tiles
    for letter, _ in selected_letters:
        for tile in tile_instances:
            if tile.letter == letter:
                tile.tiles_withdrawn()
                break

    return selected_letters

def highest_point_word(tile_instances):
    max_score = 0
    best_word = ""

    for tile in tile_instances:
        if not tile.is_empty():
            current_score = tile.points * tile.tile_count
            if current_score > max_score:
                max_score = current_score
                best_word = tile.letter

    return best_word, max_score

def compare_score(computer_score, user_score):
    print(f"Computer's score: {computer_score}, Your score: {user_score}")

def ready_input() -> str:
    r_input = input("Press Enter when ready to generate letters. "
                    "The '?' counts as any letter. "
                    "Enter 'q' to quit: ")
    if r_input.lower() == 'q':
        print("Returning to practice mode menu...")
    return r_input

def reset_tiles(tile_instances):
    for tile in tile_instances:
        tile.reset_tiles()
    print("Resetting tiles...")

def user_input_word(letters_points) -> str:
    while True:
        guess = input("Enter your word (if no valid words, press Enter with no input): ")
        if is_valid(guess, letters_points):
            return guess
        else:
            print("Invalid word. Use only the provided letters.")

def is_valid(word, available_letters):
    blank_tiles = available_letters.count(('?', 0))
    for letter, _ in word:
        if word.count((letter, 0)) > available_letters.count((letter, 0)):
            if blank_tiles > 0:
                blank_tiles -= 1
                available_letters = available_letters.replace(('?', 0), (letter, 0), 1)
                continue
            return False
    return True


def no_points_generate_letters(amount=7):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    return random.sample(alphabet, amount)

def longest_words(letters):
    english_word_list = []
    for word in twl.anagram(letters):
        english_word_list.append(word)

    if english_word_list:
        max_len = len(max(english_word_list, key=len))
        max_words = [word for word in english_word_list if len(word) == max_len]
        return max_words
    else:
        return "No valid word found."

def calculate_word_score(word, tile_instances):
    total_score = 0
    for letter, _ in word:
        for tile in tile_instances:
            if letter == tile.letter:
                total_score += tile.points
                break  # Break once you find the matching letter
    return total_score

def user_input_word(letters_points):
    while True:
        guess = input("Enter your word (if no valid words, press Enter with no input): ")
        if is_valid(guess, [letter for letter, _ in letters_points]):
            return guess
        else:
            print("Invalid word. Use only the provided letters.")


def is_valid(word, available_letters):
    for letter in word:
        if word.count(letter) > available_letters.count(letter):
            return False
    return True


def ready_input() -> str:
    """
    Asks the user if they want to do the selected mode again
    :return: Users input as a string. Anything except only 'q' will continue the practice
    """

    r_input = input("Press Enter when ready to generate letters. "
                    "The '?' counts as any letter. "
                    "Enter 'q' to quit: ")
    if r_input.lower() == 'q':
        print("Returning to practice mode menu...")
    return r_input

def reset_tiles():
    # Additional function to reset the tiles, if needed
    print("Resetting tiles...")


def user_input_word(letters: str) -> str:
    """
    Asks the user to enter their guess for best word based on letters

    :param letters: Available letters to make a word out of. ? represent any letter
    :return: A string that is either "" or only has letters from `letters` param
    """

    while True:
        guess = input("Enter your word (if no valid words, press Enter with no input): ")
        if is_valid(guess, letters):
            return guess
        else:
            print("Invalid word. Use only the provided letters.")

def no_points_generate_letters(amount: int = 7) -> str:
    """
    Generate a string of random letters, no points associated
    ? represents blank tiles which can be used as any letter

    :param amount: Number of letters to return
    :return: A string of letters that are to be used to make a word
    """

    alphabet = 'abcdefghijklmnopqrstuvwxyz?'
    return ''.join(random.sample(alphabet, amount))


def longest_words(letters: str) -> list | str:
    """
    Creates a list of the longest words based on available letters, or says if there are no valid words

    :param letters: Available letters to make words from
    :return: A list of longest words, or a string saying no words can be made from the letters
    """
    
    english_word_list = []
    for word in twl.anagram(letters):
        english_word_list.append(word)

    if english_word_list:
        max_len = len(max(english_word_list, key=len))
        max_words = [word for word in english_word_list if len(word) == max_len]
        return max_words
    else:
        return "No valid word found."

if __name__ == "__main__":
    main()