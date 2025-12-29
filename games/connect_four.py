from .base_game import BaseGame
from typing import List, Optional
import numpy as np


class ConnectFour(BaseGame):
    def __init__(self):
        super().__init__()
        self.rows = 6
        self.cols = 7
        self.initialize_board()

    def initialize_board(self):
        self.board = np.zeros((self.rows, self.cols), dtype=int)
        self.current_player = 1
        self.game_over = False
        self.winner = None

    def make_move(self, column: int) -> bool:
        if column < 0 or column >= self.cols:
            return False

        for row in range(self.rows - 1, -1, -1):
            if self.board[row, column] == 0:
                self.board[row, column] = self.current_player
                self.check_game_state()
                self.switch_player()
                return True
        return False

    def get_valid_moves(self) -> List[int]:
        return [col for col in range(self.cols) if self.board[0, col] == 0]

    def check_winner(self) -> Optional[int]:
        # Check horizontal
        for row in range(self.rows):
            for col in range(self.cols - 3):
                if (self.board[row, col] == self.board[row, col + 1] ==
                        self.board[row, col + 2] == self.board[row, col + 3] != 0):
                    return self.board[row, col]

        # Check vertical
        for row in range(self.rows - 3):
            for col in range(self.cols):
                if (self.board[row, col] == self.board[row + 1, col] ==
                        self.board[row + 2, col] == self.board[row + 3, col] != 0):
                    return self.board[row, col]

        # Check diagonal (positive slope)
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                if (self.board[row, col] == self.board[row + 1, col + 1] ==
                        self.board[row + 2, col + 2] == self.board[row + 3, col + 3] != 0):
                    return self.board[row, col]

        # Check diagonal (negative slope)
        for row in range(3, self.rows):
            for col in range(self.cols - 3):
                if (self.board[row, col] == self.board[row - 1, col + 1] ==
                        self.board[row - 2, col + 2] == self.board[row - 3, col + 3] != 0):
                    return self.board[row, col]

        return None

    def is_draw(self) -> bool:
        return len(self.get_valid_moves()) == 0 and self.check_winner() is None

    def check_game_state(self):
        winner = self.check_winner()
        if winner is not None:
            self.game_over = True
            self.winner = winner
        elif self.is_draw():
            self.game_over = True
            self.winner = 0

    def display_board(self) -> str:
        symbols = {0: ' ', 1: 'X', 2: 'O'}
        board_str = "\n"
        for i in range(self.rows):
            row = [symbols[self.board[i, j]] for j in range(self.cols)]
            board_str += "| " + " | ".join(row) + " |\n"
        board_str += "-" * (self.cols * 4 - 1) + "\n"
        board_str += "  " + "   ".join(map(str, range(self.cols))) + "\n"
        return board_str