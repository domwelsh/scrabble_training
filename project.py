import random
import twl


class Tile:
    """
    Tiles that are used in the boardgame Scrabble.

    :param letter: The letter of the tile
    :param tile_count: The number of tiles of the letter available in the bag
    :param points_value: The number of points scored each time the letter is used
    """
    def __init__(self, letter: str, tile_count: int = 0, points_value: int = 0):
        if not letter:
            raise TypeError("Missing letter")
        self.letter = letter
        self.tile_count = tile_count
        self.points_value = points_value
        self.max_tile_count = tile_count

    @property
    def letter(self):
        """Get or set letter. Letter must be set as a single alphabetical or ? character"""
        return self._letter
    
    @letter.setter
    def letter(self, letter: str):
        if isinstance(letter, str) == False:
            raise TypeError("Needs to be a string")
        elif len(letter) > 1:
            raise ValueError("Must be a single letter")
        elif not letter.isalpha() and letter != "?":
            raise ValueError("Needs to be an actual letter, or the ? symbol")
        else:
            self._letter = letter

    @property
    def tile_count(self):
        """Get or set tile count. Tile count must be set as an int > 0"""
        return self._tile_count
    
    @tile_count.setter
    def tile_count(self, tile_count: int):
        if isinstance(tile_count, int) == False:
            raise TypeError("Needs to be an int")
        elif tile_count < 0:
            raise ValueError("Cannot have negative amount of tiles")
        elif hasattr(self, "max_tile_count") and tile_count > self.max_tile_count:
            raise ValueError("Cannot have more tiles than maximum amount")
        else:
            self._tile_count = tile_count
    
    @property
    def points_value(self):
        """Get or set points value. Points value must be set as an int > 0"""
        return self._points_value
    
    @points_value.setter
    def points_value(self, points_value: int):
        if isinstance(points_value, int) == False:
            raise TypeError("Needs to be an int")
        elif points_value < 0:
            raise ValueError("Points cannot be negative")
        else:
            self._points_value = points_value

    def __str__(self):
        """Return information about the tile instance when it is called upon as a str"""
        return f"Tile {self.letter}: {self.tile_count} remaining, {self.points_value} points per tile"

    def tiles_withdrawn(self) -> None:
        """Reduces current tile count by 1, to a minimum of 0"""
        if self.tile_count > 0:
            self.tile_count -= 1

    def is_empty(self) -> bool:
        """Checks if there are any tiles remaining in the bag"""
        return self.tile_count == 0

    def reset_tiles(self) -> None:
        """Resets the number of tiles in the bag to the maximum number of tiles"""
        self.tile_count = self.max_tile_count


def main():
    print("Welcome to English Scrabble Training!")
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
        print("1. Show all longest words from 7 random letters")
        print("2. Enter your guess for the longest word from 7 random letters")
        print("3. Enter your guess for the highest scoring word, using tiles from a Scrabble bag")
        print("q. Quit")
        user_choice = input("Enter the mode number: ").strip()


def mode_1():
    """Practice mode of longest words from 7 random letters"""
    print("Entering Practice Mode 1...")
    while True:
        if ready_input() == 'q':
            break

        letters = generate_letters_random()
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
    """Practice mode of user entering their guess for the longest word from 7 random letters"""
    print("Entering Practice Mode 2...")
    while True:
        if ready_input() == 'q':
            break

        letters = generate_letters_random()
        print("Generated Letters:", ' '.join(letters))
        
        guess = user_input_word(letters)
        correct_words = longest_words(letters)

        mode_2_results(correct_words, guess)


def mode_3():
    """Practice mode of user entering their guess for the highest scoring word, using tiles from a Scrabble bag"""
    print("Entering Practice Mode 3...")

    # Create instances of Tile based on create_tiles list
    tile_instances = tuple([Tile(letter, count, points) for letter, count, points in create_tiles()])

    while True:
        if ready_input() == 'q':
            break

        # Generate letters using Tile instances
        only_letters = generate_letters_tiles(tile_instances)
        print("Generated Letters and Points:")
        for letter in only_letters:
            for tile in tile_instances:
                if tile.letter == letter:
                    print(f"{letter} ({tile.points_value} pts)")

        # Get user's word guess
        guess = user_input_word(only_letters)

        # Calculate total score for the user's guess
        total_score = calculate_word_score(guess, tile_instances)
        if guess == "":
            print("You guessed there are no valid words")
        else:
            print(f"You guessed '{guess}' for {total_score}")

        highest_score_words = highest_point_words(only_letters, tile_instances)

        mode_3_results(highest_score_words, guess, total_score)
            
        # Option to reset tiles
        tiles_in_bag = tiles_remaining(tile_instances)
        if tiles_in_bag < 7:
            print(f"You have reached the end of the bag")
            refill_bag(tile_instances)
        else:
            print(f"There are {tiles_in_bag} tiles left in the bag.")
            reset_option = input("Enter 'y' to refill the bag, or press Enter to continue: ").strip()
            if reset_option.lower() == 'y':
                refill_bag(tile_instances)


# Used in all modes
def ready_input() -> str:
    """
    Asks the user if they want to do the selected mode again

    :return: Users input as a string. Anything except only 'q' will continue the practice
    """
    print()
    r_input = input("Press Enter when ready to generate letters. "
                    "The '?' counts as any letter. "
                    "Enter 'q' to quit: ").strip()
    if r_input.lower() == 'q':
        print("Returning to practice mode menu...")
    return r_input


# Used in modes 1 and 2
def generate_letters_random(amount: int = 7) -> str:
    """
    Generate a string of random letters.
    ? represents blank tiles which can be used as any letter

    :param amount: Number of letters to return
    :return: A string of letters that are to be used to make words
    """
    alphabet = 'abcdefghijklmnopqrstuvwxyz?'
    return ''.join(random.sample(alphabet, amount))


# Used in modes 1 and 2
def longest_words(letters: str) -> list | str:
    """
    Creates a list of the longest words based on available letters, or says if there are no valid words

    :param letters: Available letters to make words from
    :return: A list of longest words, or a string saying no words can be made
    """
    word_list = all_words_list(letters)

    if word_list:
        max_len = len(max(word_list, key=len))
        max_words = [word for word in word_list if len(word) == max_len]
        return max_words
    else:
        return "No valid word found."
    

# Used in longest_words() and highest_point_words()
def all_words_list(letters: str) -> list:
    """
    Uses twl.anagram() to return a list of all Scrabble words that can be made from the letters.
    Considers ? to represent any letter.
    """
    available_words_list = []
    for word in twl.anagram(letters):
        available_words_list.append(word)
    return available_words_list


# Used in modes 2 and 3
def user_input_word(letters: str) -> str:
    """
    Asks the user to enter their guess for best word based on letters

    :param letters: Available letters to make a word out of. ? represent any letter
    :return: A string that is either "" or only has letters from `letters` param
    """
    while True:
        guess = input("Enter your word (if no valid words, press Enter with no input): ").strip().lower()
        if guess == "":
            return guess
        else:
            if is_valid(guess, letters):
                if twl.check(guess):
                    return guess
                else:
                    print("Invalid word. Not in the dictionary")
            else:
                print("Invalid word. Use only the provided letters.")


# Used in user_input_word()
def is_valid(word: str, available_letters: str) -> bool:
    """
    Checks if the user's input is a valid word based on available letters

    :param word: User's word they inputted
    :param available_letters: Valid letters to use, ? means any letter
    """
    blank_tiles = available_letters.count('?')
    for letter in word:
        if not letter.isalpha():
            return False
        elif word.count(letter) > available_letters.count(letter):
            if blank_tiles > 0:
                blank_tiles -= 1
                available_letters = available_letters.replace('?', letter, 1)
                continue
            return False
    return True


# Used in mode 2
def mode_2_results(correct_words: str | list, guess: str) -> None:
    """
    Prints response based on if there are valid words and if the user guessed correctly

    :param correct_words: Either a string saying there a no valid words, or a list of longest words
    :param guess: The user's guess for longest word
    """
    if isinstance(correct_words, str) and guess == "":
        print(f"Correct. {correct_words}")
    elif isinstance(correct_words, str) and guess != "":
        print(f"Incorrect. {correct_words}")
    elif len(guess) == len(correct_words[0]):
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


# All following functions are only used in Mode 3

def create_tiles() -> list:
    """List of tiles to be created using Tile Class"""
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
    return tiles_to_generate


def generate_letters_tiles(tile_instances: list, amount: int = 7) -> str:
    """
    Generate a string of random letters, sample is weighted based on remaining tiles.
    ? represents blank tiles which can be used as any letter

    :param amount: Number of letters to return
    :return: A string of letters that are to be used to make words
    """
    weighted_letters = ''.join(tile.letter * tile.tile_count for tile in tile_instances if not tile.is_empty())
    selected_letters = ''.join(random.sample(weighted_letters, amount))
    multiple_tiles_withdrawn(selected_letters, tile_instances)
    return selected_letters


def multiple_tiles_withdrawn(letters: str, tile_instances: list) -> None:
    """Reduce the tile count of used letters"""
    for letter in letters:
        for tile in tile_instances:
            if tile.letter == letter and not tile.is_empty():
                tile.tiles_withdrawn()
                break


def calculate_word_score(word: str, tile_instances: list) -> int:
    """Return total score of the word based on the point value of each letter"""
    total_score = 0
    for letter in word:
        for tile in tile_instances:
            if letter == tile.letter:
                total_score += tile.points_value
                break  # Break once you find the matching letter
    return total_score


def highest_point_words(letters: str, tile_instances: list) -> tuple | str:
    """
    Create a list of the highest scoring words based on available letters, or says if there are no valid words

    :param letters: Available letters to make words from
    :param tile_instances: List of tile instances
    :return: A tuple with list of highest scoring words and the max score as an int, or a string saying no words can be made
    """
    max_score = 0
    best_words = []
    word_list = all_words_list(letters)

    if word_list:
        for word in word_list:
            current_score = calculate_word_score(word, tile_instances)
            if current_score > max_score:
                max_score = current_score
                best_words.clear()
                best_words.append(word)
            elif current_score == max_score:
                best_words.append(word)
        return best_words, max_score
    else:
        return "No valid word found."


def mode_3_results(highest_score_words: str | tuple, guess: str, user_score: int) -> None:
    """
    Prints response based on if there are valid words and if the user guessed correctly

    :param highest_score_words: Either a string saying there a no valid words, or a list of words with highest score
    :param guess: The user's guess for highest scoring word
    """
    if isinstance(highest_score_words, str) and guess == "":
        print(f"Correct! {highest_score_words}")
    elif isinstance(highest_score_words, str) and guess != "":
        print(f"Incorrect. {highest_score_words}")
    else:
        highest_words = highest_score_words[0]
        highest_score = highest_score_words[1]
        if user_score == highest_score:
            if len(highest_words) == 1:
                print(f"Correct! You guessed the highest word!")
            else:
                print(f"Correct! Other words with the same score are:")
                for word in highest_words:
                    print(word)
        else:
            print(f"Incorrect. The computer's highest score was {highest_score}.")
            if len(highest_words) == 1:
                print(f"The word was:")
                print(highest_words[0])
            else:
                print(f"The words are:")
                for word in highest_words:
                    print(word)


def tiles_remaining(tile_instances: list) -> int:
    """Returns total tiles left"""
    remaining_tiles = 0
    for tile in tile_instances:
        remaining_tiles += tile.tile_count
    return remaining_tiles
        

def refill_bag(tile_instances: list) -> None:
    """Resets tiles to their max_tile_count"""
    for tile in tile_instances:
        tile.reset_tiles()
    print("Refilling bag...")


if __name__ == "__main__":
    main()
