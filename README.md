# Scrabble Training

We created the Scrabble Training program that enhances the user’s ability to find the best words from random letters through interactive practice sessions. The program has three practice modes to help users improve their performance in the game, focusing on identifying the longest words and the highest scoring words that can be made from the provided letters.

## Installation

To use the Scrabble Training program, clone this repository onto your local machine that has the latest version of Python installed. The library **random** must be installed to use the trainer, and the library **pytest** must be installed to run some of the tests. These both can be installed through pip. Once installed, use Python to run the file *`project.py`*.

## Usage

Scrabble Training offers three practice modes, which the user selects from a main menu. After some discussion amongst the team, we found that these “practice modes” were the most interesting and useful for our Scrabble program. The modes also allowed us to more easily divide the tasks needed to create a thorough program.

### Main Menu

The main menu is a While Loop that asks the user to select one of the 3 modes by inputting the cooresponding number, or entering 'q' to quit the program. The user is returned to this menu when they quit out of one of the practice modes.

### Mode 1: Longest words from 7 random letters

Mode 1 was created with the purpose of practicing the longest words to put together from the random letters generated. 

The `mode_1()` function starts by generating a printed message and then beginning a While Loop, which continues running until explicitly broken out of. At the beginning of the loop, it checks for user wants to continue by calling `ready_input()`. If the user enters 'q', the loop is terminated and the user is returned to the main menu. After confirming that the user wants to continue, the function generates 7 random letters using `generate_letters_random()`, which are then printed to the console, separated by spaces. When the user is ready to continue by pressing Enter, `longest_words()` is used to get the longest words that can be formed with the generated letters. This function will return either a string saying there are no valid words to be made from the letters, or a list of all possible words that are the longest length. These results are printed to the user, and then the loop starts again

### Mode 2: Longest word from 7 random letters with user input

The next option in the program is to opt for Mode 2, a more advanced version of Mode 1. In this mode, the user enters their guess for the longest word that can be formed from a set of 7 random letters, and the program will let them know if their guess was correct or not.

The `mode_2()` function is also a While Loop, that uses `ready_input()` to check if the user wants to continue or return to the main menu. For each iteration, the function generates a set of 7 random letters using `generate_letters_random()` and displaying them to the user. The user is then prompted to input their guess for the longest word achievable with `user_input_word()`, which also checks that the words is an actual English Scrabble word and uses `is_valid()` to confirm the word can be created from the available letters. Subsequently, the actual longest words are determined using `longest_words()`. The function then tells the user if their guess was one of the longest words or not, as well as informing them of the longest word or words.

Overall, mode_2 encourages users to practice their Scrabble skills by making educated guesses for the longest words formed from a set of randomly generated letters.

### Mode 3: Highest scoring word, using tiles from a Scrabble bag, with user input

Lastly, Mode 3 allows users to guess for the highest scoring word using tiles from a simulated Scrabble bag. 

The `mode_3()` function begins by creating instances of the Tile class based on the data provided in the `create_tiles()` list, which lists the number of tiles and points value for each letter based on the official Scrabble rules. These instances are stored as a tuple in the variable `tile_instances`. Then the function starts the While Loop, which uses `ready_input()` to check if the user wants to continue or return to the main menu.

For each iteration of the loop, the function generates a set of random letters weighted based on the remaining tiles, using the `generate_letters_tiles()` function. It then prints the generated letters along with their associated point values. The user is prompted to input their word guess, again using `user_input_word()`, and then the total score for the user's guess is calculated using `calculate_word_score()`. The function then determines the highest scoring words using `highest_point_words()` and provides feedback based on the correctness of the user's guess. The user is then informed of how many tiles are remaining in the bag, and given the option to reset it, which would use `refill_bag()` to return all tiles to their maximum tile count. If there are less than 7 tiles remaining, `refill_bag()` is automatically called.

## Design Choice Reasoning

In this section, we'll talk about a couple specific design choices we made when creating the program and why we made them.

### TWL Dictionary

Originally, we were using a dictionary from the Natural Language Toolkit (NLTK) for Python. However, we found this was not an effective dictionary for our program for 2 reasons:

1. The NLTK dictionary was a full English dictionary. This meant that it has all 1 letter words, prefixes and suffixes, and even proper names in the dictionary, none of which are valid words in Scrabble.
2. There was no clear way for us to represent blank tiles, which can be used as any letter, with this dictionary.

Fortunately, we found the TWL06 Dictionary Module, created by Michael Fogleman, and licensed under the MIT License. This module uses the TWL dictionary, which is the official dictionary for Scrabble tournaments in USA and Canada. From this module, we used two methods:

1. `twl.check(word)` - Returns True if `word` exists in the TWL06 dictionary, False otherwise. We used it in `user_input_word()` to make sure the user's guess was an actual Scrabble word.
2. `twl.anagram(letters)` - Yields words that can be formed with some or all of the given `letters`. `letters` may include '?' characters as a wildcard. We used it in `all_words_list()` to create a list of all possible words that could be made from the provided letters.

We downloaded the *`twl.py`* file from the creator's GitHub and added it to our repository to use in *`project.py`*. Using this module saved us a huge amount of time, both in providing a dictionary of only the words we want but also already having the wildcard character functionality built out.

[TWL06 GitHub repository](https://github.com/fogleman/TWL06/)

[ActiveState Code (with License)](https://code.activestate.com/recipes/577835-self-contained-twl06-dictionary-module-500-kb/)

### Tile Class

We knew we wanted to create a Tile Class, so that we could modify the state of each letter to show how many were available in the Scrabble bag. Originally, we were originally going to only have `tile_count` and `points_value` be the Instance Attributes, and the letter would be the name of the Instances. For example:
```
a = Tile(9, 1)
b = Tile(2, 3)
c = Tile(2, 3)
...
```
The idea was then to refer to the Instances when letters were used by calling the Instance's name, such as:
```
for letter in 'abc':
    letter.tiles_withdrawn()
```
However, we quickly realized this wouldn't work, as the string `'a'` is not the same as the Tile Instance `a`. So we added `letter` as an Instance Attribute.

This then led to another realization, which was the difficulty of identifying an Instance based on one of it's Attributes. For example, if we wanted to find the Tile Instance for `'i'`, in order to identify the Instance where `self.letter = 'i'`, we would need to iterate over every Tile Instance until we found the correct Instance, in loops such as:
```
for letter in 'i':
    for tile in list_of_all_tile_instances:
        if letter == tile.letter:
            tile.tiles_withdrawn()
```
What this meant for us is that any time we wanted to call upon a Tile Instance, we would need to iterate over all Instances to find the correct tile. This is when we made the decision of not setting up our Tile Instances in the "standard" way (ie `instance_name = Class(attributes)`), but rather create a list of tuples with the Attibutes of each Instance (in `create_tiles()`). We then used list comprehension to create a list of the Instances, turned that list into a tuple for additional protection, and stored it in the variable `tile_instances`. This meant that each Instance doesn't have a standard Instance name, but rather it's called upon by it's position in `tile_instances`. We were okay with doing it this way, because as mentioned before we knew we would always be needing to iterate over all Tile Instances any time we had to find a specific tile. 

## Conclusion

In conclusion, we believe writing this program was both a challenging and fun project. Team member, Dominic, deserves lots of credit for outlining the program and helping the rest of the team through their coding difficulties. All in all, we are proud of our Scrabble Training program and its design.

Thank you!

