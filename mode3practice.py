import random
import twl


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
        elif user_choice == 'q':
            print("Thanks for playing! Goodbye.")
            break
        else:
            print("Invalid choice. Please try again.")
        print("Select a mode:")
        print("1. Show all longest words")
        print("2. Enter your longest word guesses")
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


def is_valid(word: str, available_letters: str) -> bool:
    """
    Checks if the user's input is a valid word based on available letters

    :param word: User's word they inputted
    :param available_letters: Valid letters to use, ? means any letter
    """

    blank_tiles = available_letters.count('?')
    for letter in word:
        if word.count(letter) > available_letters.count(letter):
            if blank_tiles > 0:
                blank_tiles -= 1
                available_letters = available_letters.replace('?', letter, 1)
                continue
            return False
    return True


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
