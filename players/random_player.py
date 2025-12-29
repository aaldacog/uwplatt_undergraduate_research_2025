from .base_player import BasePlayer
import random

class RandomPlayer(BasePlayer):
    def get_move(self, game):
        valid_moves = game.get_valid_moves()
        return random.choice(valid_moves)