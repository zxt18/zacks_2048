import random
from base_ai_engine_2048 import AIEngine2048
from utils import Keys2048
import logging

LOG = logging.getLogger(__name__)


class Game2048:
    def __init__(
        self,
        grid_size=4,
        numbers_to_be_generated=(2, 4),
        max_score=2048,
        ai_engine: AIEngine2048 = None,
    ):
        self.grid_size = grid_size
        self.board = [[0] * grid_size for _ in range(grid_size)]
        self.numbers_to_be_generated = numbers_to_be_generated
        self.max_score = max_score
        self._end_game = 0

        if ai_engine:
            self.ai_engine = ai_engine
            LOG.info(f"AI Engine deployed : {self.ai_engine}")

    def __repr__(self):
        return f"{self.board}"

    def is_end_game(self):
        return self._end_game

    def recommend_next_move(self) -> Keys2048:
        move = self.ai_engine.recommend_next_move(self.board)
        LOG.info(f"{self.ai_engine} recommends {move}")
        return move

    def generate_tile(self) -> None:
        """
        Adds a random tile on the board, at '0' locations, from possible numbers_to_be_generated
        """
        empty_cells = [
            (i, j)
            for i in range(self.grid_size)
            for j in range(self.grid_size)
            if self.board[i][j] == 0
        ]
        if empty_cells:
            generated_coordinate = random.choice(empty_cells)
            num_generated = random.choice(self.numbers_to_be_generated)
            x, y = generated_coordinate[0], generated_coordinate[1]
            self.board[x][y] = num_generated

    def start_game(self):
        self._end_game = 0
        self.board = [[0] * self.grid_size for _ in range(self.grid_size)]

        num_of_2s = random.randint(1, self.grid_size**2)
        coordinates = [
            (i, j)
            for i in range(self.grid_size)
            for j in range(self.grid_size)
        ]
        starting_twos = random.sample(coordinates, num_of_2s)
        for x, y in starting_twos:  # coo stands for coordinate
            self.board[x][y] = 2

    def is_game_win(self):
        if any(
            v == self.max_score
            for board_list in self.board
            for v in board_list
        ):
            self._end_game = 1
            return True

    def is_game_over(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.board[i][j] == 0:
                    return (
                        False  # early termination if there are any empty cells
                    )

        # check horizontal game over
        for i in range(self.grid_size):
            for j in range(self.grid_size - 1):
                if self.board[i][j] == self.board[i][j + 1]:
                    return False

        # check vertical game over
        for i in range(self.grid_size - 1):
            for j in range(self.grid_size):
                if self.board[i][j] == self.board[i + 1][j]:
                    return False
        self._end_game = 2
        return True

    def slide_row_left(self, row):
        # [2,2,0,0] -> [4,0,0,0]
        # Transformation : [2,2] -> [4] -> [4,0,0,0]

        new_row = [num for num in row if num != 0]

        i = 0
        while i < len(new_row) - 1:
            if new_row[i] == new_row[i + 1]:
                new_row[i] = new_row[i] * 2
                new_row.pop(i + 1)
                new_row.append(0)
                i += 1
            else:
                i += 1
        new_row.extend([0] * (self.grid_size - len(new_row)))
        return new_row

    def move_left(self):
        new_board = [self.slide_row_left(row) for row in self.board]
        is_changed = new_board != self.board
        self.board = new_board
        return is_changed

    def move_right(self):
        flipped_board = [row[::-1] for row in self.board]
        new_board = [self.slide_row_left(row)[::-1] for row in flipped_board]
        is_changed = new_board != self.board
        self.board = new_board
        return is_changed

    def transpose(self):
        new_board = [[0] * self.grid_size for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                new_board[j][i] = self.board[i][j]
        self.board = new_board

    def move_up(self):
        self.transpose()
        is_changed = self.move_left()
        self.transpose()
        return is_changed

    def move_down(self):
        self.transpose()
        is_changed = self.move_right()
        self.transpose()
        return is_changed
