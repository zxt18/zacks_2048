from unittest.mock import Mock
from src.game_2048 import Game2048
from src.base_ai_engine_2048 import AIEngine2048
import pytest

@pytest.fixture
def game():
    def _create_game(board=None):
        ai_engine = Mock(spec=AIEngine2048)
        return Game2048(grid_size=4, board=board, numbers_to_be_generated=(2, 4), max_score=2048, ai_engine=ai_engine)
    return _create_game

def test_game_init(game):
    game = game()
    assert game.grid_size == 4
    assert game.numbers_to_be_generated == (2,4)
    assert game.max_score == 2048
    assert game.is_end_game() == 0 
    assert game.ai_engine is not None

def test_game_init_custom_board(game):
    custom_board = [[2, 4, 8, 16], [32, 64, 128, 256], [512, 512, 256, 128], [64, 32, 16, 8]]
    game = game(board=custom_board)
    assert game.board == custom_board
    assert game.grid_size == 4
    assert game.is_end_game() == 0

    
def test_start_game(game):
    game = game()
    assert game.is_end_game() == 0
    assert game.board == [[0] * game.grid_size for _ in range(game.grid_size)]

def test_generate_tile_all_zero(game):
        custom_board = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
        game = game(custom_board)
        game.generate_tile()
        non_zero_count = 0 
        for row in game.board :
            for cell in row : 
                if cell != 0 :
                    non_zero_count += 1
                    assert cell in game.numbers_to_be_generated

        assert non_zero_count == 1

def test_generate_tile_full_board(game):
    full_board = [[2, 4, 8, 16], [32, 64, 128, 256], [512, 512, 256, 128], [64, 32, 16, 8]]
    game = game(board=full_board)
    game.generate_tile()
    assert game.board == full_board     

def test_is_game_win(game):
    board_1 = [[2, 4, 8, 16], [32, 64, 128, 256], [512, 512, 256, 128], [64, 32, 16, 8]]
    game1 = game(board=board_1)
    assert game1.is_game_win() == False
    
    board_2 = [[2048,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
    game2 = game(board=board_2)
    assert game2.is_game_win() == True
               

    
    
    

    