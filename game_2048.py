import random


class Game2048:
    def __init__(self, grid_size=4, numbers_to_be_generated=(2, 4)):
        self.grid_size = grid_size
        self.board = [[0] * grid_size for _ in range(grid_size)]
        self.score = 0
        self.numbers_to_be_generated = numbers_to_be_generated

    def __repr__(self):
        return f"Current score : {self.score}\n {self.board}"

    def generate_tile(self) -> None:
        coordinates = []
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    coordinates.append((i, j))

        if not coordinates:
            return
        else:
            generated_coordinate = random.choice(coordinates)
            num_generated = random.choice(self.numbers_to_be_generated)
            x, y = generated_coordinate[0], generated_coordinate[1]
            self.board[x][y] = num_generated

    def start_game(self):
        num_of_2s = random.randint(1, self.grid_size**2)
        coordinates = [
            (i, j)
            for i in range(self.grid_size)
            for j in range(self.grid_size)
        ]
        starting_twos = random.sample(coordinates, num_of_2s)
        for coo in starting_twos:  # coo stands for coordinate
            x, y = coo
            self.board[x][y] = 2

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
        return True

    def slide_row_left(self, row):
        # [2,2,0,0] -> [4,0,0,0]
        # Transformation : [2,2] -> [4] -> [4,0,0,0]
        new_row = [num for num in row if num != 0]

        i = 0
        while i < len(new_row) - 1:
            if new_row[i] == new_row[i + 1]:
                new_row[i] = new_row[i] * 2
                self.score += new_row[i]
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
        for i in range(len(self.grid_size)):
            for j in range(len(self.grid_size[0])):
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
