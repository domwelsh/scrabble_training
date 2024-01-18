import pytest
from project import Tile, ready_input, user_input_word, is_valid, longest_words, generate_letters_tiles, generate_letters_random, calculate_word_score, highest_point_words, all_words_list, multiple_tiles_withdrawn


def test_ready_input(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '     q     ')
    assert ready_input() == 'q'
    monkeypatch.setattr('builtins.input', lambda _: 'Q')
    assert ready_input() == 'Q'
    

def test_user_input_word(monkeypatch):
    letters = 'abcd'
    monkeypatch.setattr('builtins.input', lambda _: '         ')
    assert user_input_word(letters) == ''
    monkeypatch.setattr('builtins.input', lambda _: '  CAB  ')
    assert user_input_word(letters) == 'cab'

    int_letters = 12
    monkeypatch.setattr('builtins.input', lambda _: '12')
    with pytest.raises(AttributeError):
        user_input_word(int_letters) == '12'

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
    tile_a = Tile('a', 5, 2)
    tile_b = Tile('b', 20, 0)
    tile_c = Tile('c', 10, 3)
    tile_iterable = [tile_a]
    with pytest.raises(ValueError):
        generate_letters_tiles(tile_iterable)


def test_calculate_word_score():
    tile_a = Tile('a', 10, 10)
    tile_b = Tile('b', 10, 5)
    tile_iterable = [tile_a, tile_b]
    assert calculate_word_score("aaaaaa", tile_iterable) == 60
    assert calculate_word_score("cdccd", tile_iterable) == 0
    with pytest.raises(TypeError):
            calculate_word_score(123, tile_iterable) == 0


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
    assert highest_point_words(letters, tile_iterable) [1] == 10
    assert highest_point_words(letters, tile_iterable) == (['mauve', 'mavie'], 10)
    with pytest.raises(TypeError):
        highest_point_words(1, tile_iterable) == 10
        highest_point_words(letters, tile_iterable) == (['mauve', 'mavie'], 10)
        highest_point_words('', tile_iterable) == 10




def test_all_words_list():
    letters = "see"
    tile_s = Tile('s', 4, 1)
    tile_e = Tile('e', 12, 1)
    assert 'see' in all_words_list(letters)
    assert 'es' in all_words_list(letters)
    assert all_words_list(letters) == ['es', 'see']



def test_multiple_tiles_withdrawn():
    pass

def test_tile_initialization():
    tile = Tile('a', 9, 1)
    assert tile.letter == 'a'
    assert tile.tile_count == 9
    assert tile.points_value == 1
    assert tile.max_tile_count == 9
    with pytest.raises(ValueError):
        tile2 = Tile(3, 2, 1)
    with pytest.raises(ValueError):
        tile3 = Tile('b', 'd', 1)
    with pytest.raises(ValueError):
        tile4 = Tile('c', 2, -1)

def test_tile_withdrawn():
    tile = Tile('a', 9, 1)
    tile.tiles_withdrawn()
    assert tile.tile_count == 8

def test_tile_is_empty():
    # Test for a case where tile_count is 0
    tile1 = Tile('a', 0, 1)
    assert tile1.is_empty()

def test_tile_reset_tiles():
    tile = Tile('a', 5, 1)
    tile.tiles_withdrawn()
    tile.reset_tiles()
    assert tile.tile_count == 5
    
def test_tile_invalid_letter():
    with pytest.raises(ValueError, match="Needs to be a string"):
        Tile(123, 5, 2)


def test_tile_negative_tile_count():
    with pytest.raises(ValueError, match="Cannot have negative amount of tiles"):
        Tile('a', -5, 2)

def test_tile_negative_points_value():
    with pytest.raises(ValueError, match="Points cannot be negative"):
        Tile('a', 5, -2)

def test_tile_withdrawn_zero_count():
    # Create a Tile instance with tile_count set to 0
    tile = Tile('a', 0, 1)
    # Attempt to withdraw a tile
    tile.tiles_withdrawn()
    # Ensure that the tile_count remains 0
    assert tile.tile_count == 0
    # Ensure that is_empty still returns True
    assert tile.is_empty()
    
