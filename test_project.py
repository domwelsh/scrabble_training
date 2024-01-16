import pytest
from project import ready_input, user_input_word, is_valid, longest_words, generate_letters_tiles, generate_letters_random, calculate_word_score, highest_point_word, all_words_list


def test_ready_input():
    # Dom - I'll take care of this one
    pass


def test_user_input_word():
    # Dom - I'll take care of this one
    pass


def test_is_valid():
    assert is_valid("corn", "tnoarec") == True
    assert is_valid("cron", "tnoaecs") == False
    # Add more tests, especially corner cases


def test_longest_words():
   assert longest_words("act") == ["act", "cat"]
   assert longest_words("abcd") != [] and isinstance(longest_words("abcd"), list)
   assert longest_words("xyz") == "No valid word found."
   # Add more tests, especially corner cases


def test_generate_letters_random():
    assert len(generate_letters_random()) == 7 and isinstance(generate_letters_random(), str)
    assert generate_letters_random(0) == ""
    with pytest.raises(ValueError):
        generate_letters_random(-1)
    # Add more tests, especially other corner cases


def test_generate_letters_tiles():
    pass


def test_calculate_word_score():
    pass


def test_highest_point_word():
    pass


def test_all_words_list():
    pass
