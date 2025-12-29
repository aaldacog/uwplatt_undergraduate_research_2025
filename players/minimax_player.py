from games.connect_four import ConnectFour
from games.tic_tac_toe import TicTacToe
from .base_player import BasePlayer
import random


class MinimaxPlayer(BasePlayer):
    def __init__(self, player_id: int, depth: int = 3):
        super().__init__(player_id)
        self.depth = depth

    def get_move(self, game):
        valid_moves = game.get_valid_moves()

        if game.__class__.__name__ == "TicTacToe":
            return self._minimax_tic_tac_toe(game, valid_moves)
        else:
            return self._minimax_connect_four(game, valid_moves)

    def _minimax_tic_tac_toe(self, game, valid_moves):
        best_score = float('-inf')
        best_moves = []
        alpha = float('-inf')
        beta = float('inf')

        for move in valid_moves:
            # Make a copy of the game state
            game_copy = TicTacToe()
            game_copy.board = game.board.copy()
            game_copy.current_player = game.current_player

            game_copy.make_move(move)
            score = self._minimax(game_copy, self.depth, False, alpha, beta)

            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

            # Update alpha for the maximizing player
            alpha = max(alpha, best_score)

        return random.choice(best_moves)

    def _minimax_connect_four(self, game, valid_moves):
        best_score = float('-inf')
        best_moves = []
        alpha = float('-inf')
        beta = float('inf')

        for move in valid_moves:
            game_copy = ConnectFour()
            game_copy.board = game.board.copy()
            game_copy.current_player = game.current_player

            game_copy.make_move(move)
            score = self._minimax(game_copy, self.depth, False, alpha, beta)

            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

            # Update alpha for the maximizing player
            alpha = max(alpha, best_score)

        return random.choice(best_moves)

    def _minimax(self, game, depth, is_maximizing, alpha, beta):
        if depth == 0 or game.game_over:
            return self._evaluate(game)

        if is_maximizing:
            best_score = float('-inf')
            for move in game.get_valid_moves():
                game_copy = game.__class__()
                game_copy.board = game.board.copy()
                game_copy.current_player = game.current_player

                game_copy.make_move(move)
                score = self._minimax(game_copy, depth - 1, False, alpha, beta)
                best_score = max(score, best_score)

                # Alpha-beta pruning
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break  # Beta cut-off
            return best_score
        else:
            best_score = float('inf')
            for move in game.get_valid_moves():
                game_copy = game.__class__()
                game_copy.board = game.board.copy()
                game_copy.current_player = game.current_player

                game_copy.make_move(move)
                score = self._minimax(game_copy, depth - 1, True, alpha, beta)
                best_score = min(score, best_score)

                # Alpha-beta pruning
                beta = min(beta, best_score)
                if beta <= alpha:
                    break  # Alpha cut-off
            return best_score

    def _evaluate(self, game):
        if game.winner == self.player_id:
            return 100
        elif game.winner == 3 - self.player_id:
            return -100
        elif game.winner == 0:  # Draw
            return 0

        # Simple heuristic for ongoing games
        if game.__class__.__name__ == "TicTacToe":
            return self._evaluate_tic_tac_toe(game)
        else:
            return self._evaluate_connect_four(game)

    def _evaluate_tic_tac_toe(self, game):
        score = 0
        # Simple center control heuristic
        if game.board[1, 1] == self.player_id:
            score += 3
        return score

    def _evaluate_connect_four(self, game):
        score = 0
        # Simple center column preference
        center_col = game.cols // 2
        for row in range(game.rows):
            if game.board[row, center_col] == self.player_id:
                score += 2
        return score