from .base_game import BaseGame
from typing import List, Tuple, Optional
import numpy as np


class TicTacToe(BaseGame):
    def __init__(self):
        super().__init__()
        self.initialize_board()

    def initialize_board(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1
        self.game_over = False
        self.winner = None

    def make_move(self, move: Tuple[int, int]) -> bool:
        row, col = move
        if self.board[row, col] == 0:
            self.board[row, col] = self.current_player
            self.check_game_state()
            self.switch_player()
            return True
        return False

    def get_valid_moves(self) -> List[Tuple[int, int]]:
        moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i, j] == 0:
                    moves.append((i, j))
        return moves

    def check_winner(self) -> Optional[int]:
        # Check rows and columns
        for i in range(3):
            if self.board[i, 0] == self.board[i, 1] == self.board[i, 2] != 0:
                return self.board[i, 0]
            if self.board[0, i] == self.board[1, i] == self.board[2, i] != 0:
                return self.board[0, i]

        # Check diagonals
        if self.board[0, 0] == self.board[1, 1] == self.board[2, 2] != 0:
            return self.board[0, 0]
        if self.board[0, 2] == self.board[1, 1] == self.board[2, 0] != 0:
            return self.board[0, 2]

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
        for i in range(3):
            row = [symbols[self.board[i, j]] for j in range(3)]
            board_str += " " + " | ".join(row) + " \n"
            if i < 2:
                board_str += "-----------\n"
        return board_str