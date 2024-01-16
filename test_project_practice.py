# test_project_practice.py
import pytest
from project import Tile

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
