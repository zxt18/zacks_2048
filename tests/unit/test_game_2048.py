from unittest.mock import Mock
from src.game_2048 import Game2048
from src.base_ai_engine_2048 import AIEngine2048
import pytest


@pytest.fixture
def game():
    def _create_game(board=None):
        ai_engine = Mock(spec=AIEngine2048)
        return Game2048(
            grid_size=4,
            board=board,
            numbers_to_be_generated=(2, 4),
            max_score=2048,
            ai_engine=ai_engine,
        )

    return _create_game


def test_game_init(game):
    game = game()
    assert game.grid_size == 4
    assert game.numbers_to_be_generated == (2, 4)
    assert game.max_score == 2048
    assert game.is_end_game() == 0
    assert game.ai_engine is not None


def test_game_init_custom_board(game):
    custom_board = [
        [2, 4, 8, 16],
        [32, 64, 128, 256],
        [512, 512, 256, 128],
        [64, 32, 16, 8],
    ]
    game = game(board=custom_board)
    assert game.board == custom_board
    assert game.grid_size == 4
    assert game.is_end_game() == 0


def test_start_game(game):
    game = game()
    assert game.is_end_game() == 0
    assert game.board == [[0] * game.grid_size for _ in range(game.grid_size)]


def test_generate_tile_all_zero(game):
    custom_board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    game = game(custom_board)
    game.generate_tile()
    non_zero_count = 0
    for row in game.board:
        for cell in row:
            if cell != 0:
                non_zero_count += 1
                assert cell in game.numbers_to_be_generated

    assert non_zero_count == 1

def test_generate_one_tile(game):
    custom_board = [[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    game = game(custom_board)
    game.generate_tile()
    non_zero_count = 0
    for row in game.board:
        for cell in row:
            if cell != 0:
                non_zero_count += 1
                assert cell in game.numbers_to_be_generated

    assert non_zero_count == 2

def test_generate_tile_full_board(game):
    full_board = [
        [2, 4, 8, 16],
        [32, 64, 128, 256],
        [512, 512, 256, 128],
        [64, 32, 16, 8],
    ]
    game = game(board=full_board)
    game.generate_tile()
    assert game.board == full_board


def test_is_game_win(game):
    board_1 = [
        [2, 4, 8, 16],
        [32, 64, 128, 256],
        [512, 512, 256, 128],
        [64, 32, 16, 8],
    ]
    game1 = game(board=board_1)
    assert game1.is_game_win() == False

    board_2 = [[2048, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    game2 = game(board=board_2)
    assert game2.is_game_win() == True


slide_row_left_cases = [
    ([2, 2, 0, 0], [4, 0, 0, 0]),
    ([0, 0, 0, 0], [0, 0, 0, 0]),
    ([2, 0, 0, 2], [4, 0, 0, 0]),
    ([2, 2, 2, 2], [4, 4, 0, 0]),
    ([4, 0, 0, 0], [4, 0, 0, 0]),
    ([2, 4, 2, 4], [2, 4, 2, 4]),
    ([0, 2, 0, 4], [2, 4, 0, 0]),
    ([8, 8, 4, 4], [16, 8, 0, 0]),
]


@pytest.mark.parametrize("input_row, expected", slide_row_left_cases)
def test_slide_row_left(game, input_row, expected):
    game = game()
    assert game.slide_row_left(input_row) == expected


move_left_cases = [
    (
        [[2, 2, 0, 0], [0, 0, 0, 0], [2, 0, 0, 2], [0, 0, 0, 2]],
        [[4, 0, 0, 0], [0, 0, 0, 0], [4, 0, 0, 0], [2, 0, 0, 0]],
        True,
    ),
    (
        [[2, 0, 2, 0], [4, 4, 0, 0], [0, 0, 0, 0], [8, 0, 8, 0]],
        [[4, 0, 0, 0], [8, 0, 0, 0], [0, 0, 0, 0], [16, 0, 0, 0]],
        True,
    ),
    (
        [[2, 2, 2, 2], [0, 0, 0, 0], [4, 4, 4, 4], [8, 8, 8, 8]],
        [[4, 4, 0, 0], [0, 0, 0, 0], [8, 8, 0, 0], [16, 16, 0, 0]],
        True,
    ),
    (
        [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        False,
    ),
    (
        [[2, 4, 8, 16], [2, 4, 8, 16], [2, 4, 8, 16], [2, 4, 8, 16]],
        [[2, 4, 8, 16], [2, 4, 8, 16], [2, 4, 8, 16], [2, 4, 8, 16]],
        False,
    ),
]


@pytest.mark.parametrize(
    "input_board,expected_board,expected_move", move_left_cases
)
def test_move_left(game, input_board, expected_board, expected_move):
    game_instance = game(input_board)
    changed = game_instance.move_left()
    assert changed == expected_move
    assert game_instance.board == expected_board


move_right_cases = [
    (
        [[2, 2, 0, 0], [0, 0, 0, 0], [2, 0, 0, 2], [0, 0, 0, 2]],
        [[0, 0, 0, 4], [0, 0, 0, 0], [0, 0, 0, 4], [0, 0, 0, 2]],
        True,
    ),
    (
        [[2, 0, 2, 0], [4, 4, 0, 0], [0, 0, 0, 0], [8, 0, 8, 0]],
        [[0, 0, 0, 4], [0, 0, 0, 8], [0, 0, 0, 0], [0, 0, 0, 16]],
        True,
    ),
    (
        [[2, 2, 2, 2], [0, 0, 0, 0], [4, 4, 4, 4], [8, 8, 8, 8]],
        [[0, 0, 4, 4], [0, 0, 0, 0], [0, 0, 8, 8], [0, 0, 16, 16]],
        True,
    ),
    (
        [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        False,
    ),
    (
        [[2, 4, 8, 16], [2, 4, 8, 16], [2, 4, 8, 16], [2, 4, 8, 16]],
        [[2, 4, 8, 16], [2, 4, 8, 16], [2, 4, 8, 16], [2, 4, 8, 16]],
        False,
    ),
]


@pytest.mark.parametrize(
    "input_board,expected_board,expected_move", move_right_cases
)
def test_move_right(game, input_board, expected_board, expected_move):
    game_instance = game(input_board)
    changed = game_instance.move_right()
    assert changed == expected_move
    assert game_instance.board == expected_board


move_up_cases = [
    (
        [[2, 0, 2, 0], [2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[4, 0, 2, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        True,
    ),
    (
        [[2, 4, 0, 8], [2, 4, 0, 8], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[4, 8, 0, 16], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        True,
    ),
    (
        [[2, 0, 4, 0], [0, 8, 0, 16], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[2, 8, 4, 16], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        True,
    ),
    (
        [[2, 4, 8, 16], [2, 4, 8, 16], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[4, 8, 16, 32], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        True,
    ),
    (
        [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        False,
    ),
]


@pytest.mark.parametrize(
    "input_board,expected_board,expected_move", move_up_cases
)
def test_move_up(game, input_board, expected_board, expected_move):
    game_instance = game(input_board)
    changed = game_instance.move_up()
    assert changed == expected_move
    assert game_instance.board == expected_board


move_down_cases = [
    (
        [[0, 0, 0, 0], [0, 0, 0, 0], [2, 0, 0, 0], [2, 0, 2, 0]],
        [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [4, 0, 2, 0]],
        True,
    ),
    (
        [[0, 0, 0, 0], [0, 0, 0, 0], [2, 4, 0, 8], [2, 4, 0, 8]],
        [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [4, 8, 0, 16]],
        True,
    ),
    (
        [[0, 0, 0, 0], [0, 8, 0, 16], [2, 0, 4, 0], [0, 0, 0, 0]],
        [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [2, 8, 4, 16]],
        True,
    ),
    (
        [[0, 0, 0, 0], [0, 0, 0, 0], [2, 4, 8, 16], [2, 4, 8, 16]],
        [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [4, 8, 16, 32]],
        True,
    ),
    (
        [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        False,
    ),
]


@pytest.mark.parametrize(
    "input_board,expected_board,expected_move", move_down_cases
)
def test_move_down(game, input_board, expected_board, expected_move):
    game_instance = game(input_board)
    changed = game_instance.move_down()
    assert changed == expected_move
    assert game_instance.board == expected_board


is_game_win_cases = [
    ([[2048, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], True),
    ([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], False),
    ([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]], False),
]


@pytest.mark.parametrize("input_board,expected_win", is_game_win_cases)
def test_is_game_win(game, input_board, expected_win):
    game_instance = game(input_board)
    ans = game_instance.is_game_win()
    assert expected_win == ans


is_game_over_cases = [
    ([[2048, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], False),
    ([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], False),
    ([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]], True),
]


@pytest.mark.parametrize("input_board,expected_game_over", is_game_over_cases)
def test_is_game_win(game, input_board, expected_game_over):
    game_instance = game(input_board)
    ans = game_instance.is_game_over()
    assert expected_game_over == ans
