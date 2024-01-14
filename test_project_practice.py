# test_project_practice.py

from project import Tile

def test_tile_initialization():
    tile = Tile('a', 9, 1)
    assert tile.letter == 'a'
    assert tile.tile_count == 9
    assert tile.points == 1
    assert tile.max_tile_count == 9

def test_tile_withdrawn():
    tile = Tile('a', 9, 1)
    tile.tiles_withdrawn()
    assert tile.tile_count == 8

def test_tile_is_empty():
    tile = Tile('a', 0, 1)
    assert tile.is_empty()

def test_tile_reset_tiles():
    tile = Tile('a', 5, 1)
    tile.tiles_withdrawn()
    tile.reset_tiles()
    assert tile.tile_count == 5
