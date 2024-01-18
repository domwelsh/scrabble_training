import pytest
from project import (
    Tile,
    ready_input,
    user_input_word,
    is_valid, longest_words,
    generate_letters_tiles,
    generate_letters_random,
    calculate_word_score,
    highest_point_words,
    all_words_list,
    multiple_tiles_withdrawn,
    tiles_remaining,
    refill_bag,
    mode_2_results,
    mode_3_results
)


# Tests of Tile Class Methods
def test_tile_initialization():
    tile = Tile('a', 9, 1)
    assert tile.letter == 'a'
    assert tile.tile_count == 9
    assert tile.points_value == 1
    assert tile.max_tile_count == 9
    with pytest.raises(TypeError):
        tile2 = Tile()


def test_tile_invalid_letter():
    with pytest.raises(TypeError, match="Needs to be a string"):
        Tile(123, 5, 2)


def test_tile_negative_tile_count():
    with pytest.raises(ValueError, match="Cannot have negative amount of tiles"):
        Tile('a', -5, 2)


def test_tile_negative_points_value():
    with pytest.raises(ValueError, match="Points cannot be negative"):
        Tile('a', 5, -2)


def test_setting_tile_count_above_max():
    tile_a = Tile('a', 10, 0)
    assert tile_a.max_tile_count == 10
    tile_a.tile_count = 2
    assert tile_a.tile_count < tile_a.max_tile_count
    with pytest.raises(ValueError):
        tile_a.tile_count = 12


def test_tile_withdrawn():
    tile = Tile('a', 9, 1)
    tile.tiles_withdrawn()
    assert tile.tile_count == 8
    tile2 = Tile('b', 0, 1)
    tile2.tiles_withdrawn()
    assert tile2.tile_count == 0


def test_tile_is_empty():
    # Test for a case where tile_count is 0
    tile1 = Tile('a', 0, 1)
    assert tile1.is_empty()
    tile2 = Tile('b', 2, 3)
    assert not tile2.is_empty()


def test_tile_reset_tiles():
    tile = Tile('a', 5, 1)
    tile.tiles_withdrawn()
    assert tile.tile_count == 4
    tile.reset_tiles()
    assert tile.tile_count == 5
    tile.max_tile_count = -3
    with pytest.raises(ValueError):
        tile.reset_tiles()


# Tests of non-Class functions
def test_ready_input(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '     q     ')
    assert ready_input() == 'q'
    monkeypatch.setattr('builtins.input', lambda _: 'Q')
    assert ready_input() == 'Q'


def test_generate_letters_random():
    assert len(generate_letters_random()) == 7 \
        and isinstance(generate_letters_random(), str)
    assert generate_letters_random(0) == ""
    with pytest.raises(ValueError):
        generate_letters_random(-1)
    with pytest.raises(TypeError):
        generate_letters_random("12")
    

def test_longest_words():
    assert longest_words("act") == ["act", "cat"]
    assert longest_words("abcd") != [] \
        and isinstance(longest_words("abcd"), list)
    assert longest_words("xyz") == "No valid word found."
    assert len(longest_words("?????")[0]) == 5
    assert longest_words("") == "No valid word found."
    with pytest.raises(TypeError):
        longest_words(123) != []
    assert longest_words(['ab', 'cd', 'ef']) == "No valid word found."


def test_all_words_list():
    letters = "see"
    assert 'see' in all_words_list(letters)
    assert 'es' in all_words_list(letters)
    assert len(all_words_list(letters)) == 2
    assert isinstance(all_words_list("??"), list) \
        and len(all_words_list("??")) > 100
    assert all_words_list("a") == []
    assert all_words_list("") == []
    with pytest.raises(TypeError):
        all_words_list()
    with pytest.raises(TypeError):
        all_words_list(12)


def test_user_input_word(monkeypatch):
    letters = 'abcd'
    monkeypatch.setattr('builtins.input', lambda _: '         ')
    assert user_input_word(letters) == ''
    monkeypatch.setattr('builtins.input', lambda _: '  CAB  ')
    assert user_input_word(letters) == 'cab'

    int_letters = 12
    monkeypatch.setattr('builtins.input', lambda _: '12')
    with pytest.raises(AttributeError):
        user_input_word(int_letters)


def test_is_valid():
    assert is_valid("corn", "tnoarec") == True
    assert is_valid("cron", "tnoaecs") == False
    assert is_valid("????", "????") == False
    assert is_valid("example", "???????") == True
    assert is_valid("example", "????") == False
    assert is_valid("123", "tesing") == False
    assert is_valid("", "sdf") == True
    with pytest.raises(TypeError):
        is_valid(123, "some")
    with pytest.raises(AttributeError):
        is_valid("word", 123)


def test_mode_2_results(capsys):
    mode_2_results("No valid word found.", "")
    output = capsys.readouterr()
    assert output.out.strip() == "Correct. No valid word found."

    mode_2_results("Test", "Guess")
    output = capsys.readouterr()
    assert output.out.strip() == "Incorrect. Test"

    mode_2_results(['test'], 'test')
    output = capsys.readouterr()
    assert output.out.strip() == "Correct! You found the longest word."

    mode_2_results(['test', 'word'], 'word')
    output = capsys.readouterr()
    assert "Correct! You found one of the longest words." in output.out.strip() 

    mode_2_results(['test'], 'wrong')
    output = capsys.readouterr()
    assert output.out.strip() == "Incorrect. The longest word is: test"

    mode_2_results(['test', 'again'], 'stillwrong')
    output = capsys.readouterr()
    assert "Incorrect. The longest words are:" in output.out.strip()


def test_generate_letters_tiles():
    tile_a = Tile('a', 5, 2)
    tile_b = Tile('b', 20, 0)
    tile_c = Tile('c', 10, 3)
    tile_iterable = [tile_a]
    with pytest.raises(ValueError):
        generate_letters_tiles(tile_iterable)
    tile_iterable = [tile_a, tile_b, tile_c]
    assert len(generate_letters_tiles(tile_iterable)) == 7 \
        and isinstance(generate_letters_tiles(tile_iterable), str)
    assert generate_letters_tiles(tile_iterable, 0) == ""
    with pytest.raises(ValueError):
        generate_letters_tiles(tile_iterable, -1)
    with pytest.raises(TypeError):
        generate_letters_tiles(tile_iterable, "12")


def test_multiple_tiles_withdrawn():
    letters = "see"
    tile_s = Tile('s', 4, 1)
    tile_e = Tile('e', 12, 1)
    tile_t = Tile('t', 40, 2)
    tile_instances = [tile_e, tile_s]
    multiple_tiles_withdrawn(letters, tile_instances)
    assert tile_s.tile_count == 3
    assert tile_e.tile_count == 10
    assert tile_t.tile_count == 40
    s_letters = "sssssss"
    multiple_tiles_withdrawn(s_letters, tile_instances)
    assert tile_s.tile_count == 0
    with pytest.raises(TypeError):
        multiple_tiles_withdrawn(12, tile_instances)


def test_calculate_word_score():
    tile_a = Tile('a', 10, 10)
    tile_b = Tile('b', 10, 5)
    tile_c = Tile('c', 10, 0)
    tile_iterable = [tile_a, tile_b]
    assert calculate_word_score("aaaaaa", tile_iterable) == 60
    assert calculate_word_score("cdccd", tile_iterable) == 0
    with pytest.raises(TypeError):
            calculate_word_score(123, tile_iterable)
    tile_iterable = ["a", "b", "c"]
    with pytest.raises(AttributeError):
        calculate_word_score("word", tile_iterable)


def test_highest_point_words():
    letters = "iaguvme"
    tile_i = Tile('i', 9, 1)
    tile_a = Tile('a', 9, 1)
    tile_g = Tile('g', 3, 2)
    tile_u = Tile('u', 4, 1)
    tile_v = Tile('v', 2, 4)
    tile_m = Tile('m', 2, 3)
    tile_e = Tile('e', 12, 1)
    tile_iterable = [tile_i, tile_a, tile_g, tile_u, tile_v, tile_m, tile_e]
    assert highest_point_words(letters, tile_iterable)[1] == 10
    assert highest_point_words(letters, tile_iterable) == (['mauve', 'mavie'], 10)
    with pytest.raises(TypeError):
        highest_point_words(1, tile_iterable) == 10
    assert highest_point_words('', tile_iterable) == "No valid word found."
    letters = "ai"
    assert isinstance(highest_point_words(letters, tile_iterable)[0], list) \
        and len(highest_point_words(letters, tile_iterable)[0]) == 1


def test_mode_3_results(capsys):
    mode_3_results("test", "", 0)
    output = capsys.readouterr()
    assert output.out.strip() == "Correct! test"

    mode_3_results("test", "wrong", 0)
    output = capsys.readouterr()
    assert output.out.strip() == "Incorrect. test"

    mode_3_results((["test"], 10), "something", 10)
    output = capsys.readouterr()
    assert output.out.strip() == "Correct! You guessed the highest word!"

    mode_3_results((["test", "words"], 20), "something", 20)
    output = capsys.readouterr()
    assert "Correct! Other words with the same score are:" in output.out.strip()

    mode_3_results((["test"], 5), "wrong", 50)
    output = capsys.readouterr()
    assert output.out.strip() == "Incorrect. The computer's highest score was 5.\nThe word was:\ntest"

    mode_3_results((["test", "other"], 12), "", 30)
    output = capsys.readouterr()
    assert output.out.strip() == "Incorrect. The computer's highest score was 12.\nThe words are:\ntest\nother"


def test_tiles_remaining():
    tile_a = Tile('a', 10, 0)
    tile_b = Tile('b', 4, 12)
    tile_iterable = [tile_a, tile_b]
    assert tiles_remaining(tile_iterable) == 14
    tile_a.tiles_withdrawn()
    tile_a.tiles_withdrawn()
    tile_b.tiles_withdrawn()
    assert tiles_remaining(tile_iterable) == 11


def test_refill_bag():
    tile_a = Tile('a', 10, 0)
    tile_b = Tile('b', 4, 12)
    tile_iterable = [tile_a, tile_b]
    assert tiles_remaining(tile_iterable) == 14
    tile_a.tile_count = 2
    tile_b.tile_count = 0
    assert tiles_remaining(tile_iterable) == 2
    refill_bag(tile_iterable)
    assert tiles_remaining(tile_iterable) == 14
    tile_a.max_tile_count = 2
    tile_b.max_tile_count = 1
    refill_bag(tile_iterable)
    assert tiles_remaining(tile_iterable) == 3
