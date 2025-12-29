from abc import ABC, abstractmethod
from typing import List, Tuple, Any, Optional


class BaseGame(ABC):
    def __init__(self):
        self.board = None
        self.current_player = 1
        self.game_over = False
        self.winner = None

    @abstractmethod
    def initialize_board(self) -> Any:
        pass

    @abstractmethod
    def make_move(self, move: Any) -> bool:
        pass

    @abstractmethod
    def get_valid_moves(self) -> List[Any]:
        pass

    @abstractmethod
    def check_winner(self) -> Optional[int]:
        pass

    @abstractmethod
    def is_draw(self) -> bool:
        pass

    @abstractmethod
    def display_board(self) -> str:
        pass

    def switch_player(self):
        self.current_player = 3 - self.current_player  # Switches between 1 and 2

    def get_game_state(self):
        return {
            'board': self.board,
            'current_player': self.current_player,
            'game_over': self.game_over,
            'winner': self.winner
        }