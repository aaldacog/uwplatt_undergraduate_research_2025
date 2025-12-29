from abc import ABC, abstractmethod
from typing import Any


class BasePlayer(ABC):
    def __init__(self, player_id: int):
        self.player_id = player_id

    @abstractmethod
    def get_move(self, game) -> Any:
        pass

    def __str__(self):
        return f"{self.__class__.__name__} {self.player_id}"