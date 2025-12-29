from .base_player import BasePlayer
import random
import math


class AStarPlayer(BasePlayer):
    def __init__(self, player_id: int, depth: int = 3):
        super().__init__(player_id)
        self.depth = depth

    def get_move(self, game):
        valid_moves = game.get_valid_moves()

        if game.__class__.__name__ == "TicTacToe":
            return self._astar_tic_tac_toe(game, valid_moves)
        else:
            return self._astar_connect_four(game, valid_moves)

    def _astar_tic_tac_toe(self, game, valid_moves):
        best_score = float('-inf')
        best_moves = []

        for move in valid_moves:
            # Make a copy of the game state
            game_copy = type(game)()
            game_copy.board = game.board.copy()
            game_copy.current_player = game.current_player

            game_copy.make_move(move)

            # A* evaluation: f(n) = g(n) + h(n)
            g_cost = 0  # Depth cost (we want to win quickly)
            h_cost = self._heuristic_evaluation(game_copy)
            score = h_cost - g_cost  # Higher score is better

            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

        return random.choice(best_moves)

    def _astar_connect_four(self, game, valid_moves):
        best_score = float('-inf')
        best_moves = []

        for move in valid_moves:
            game_copy = type(game)()
            game_copy.board = game.board.copy()
            game_copy.current_player = game.current_player

            game_copy.make_move(move)

            g_cost = 0  # Depth cost
            h_cost = self._heuristic_evaluation(game_copy)
            score = h_cost - g_cost

            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

        return random.choice(best_moves)

    def _heuristic_evaluation(self, game):
        """Heuristic evaluation function for A* algorithm"""
        if game.game_over:
            if game.winner == self.player_id:
                return 1000  # Win
            elif game.winner == 3 - self.player_id:
                return -1000  # Loss
            else:
                return 0  # Draw

        score = 0

        if game.__class__.__name__ == "TicTacToe":
            score = self._evaluate_tic_tac_toe(game)
        else:
            score = self._evaluate_connect_four(game)

        return score

    def _evaluate_tic_tac_toe(self, game):
        score = 0

        # Evaluate rows, columns, and diagonals
        lines = []

        # Rows
        for i in range(3):
            lines.append([game.board[i, j] for j in range(3)])

        # Columns
        for j in range(3):
            lines.append([game.board[i, j] for i in range(3)])

        # Diagonals
        lines.append([game.board[i, i] for i in range(3)])
        lines.append([game.board[i, 2 - i] for i in range(3)])

        for line in lines:
            score += self._evaluate_line(line)

        # Center control
        if game.board[1, 1] == self.player_id:
            score += 3
        elif game.board[1, 1] == 3 - self.player_id:
            score -= 3

        return score

    def _evaluate_connect_four(self, game):
        score = 0

        # Evaluate all possible 4-in-a-row sequences
        for row in range(game.rows):
            for col in range(game.cols - 3):
                line = [game.board[row, col + i] for i in range(4)]
                score += self._evaluate_line(line)

        for row in range(game.rows - 3):
            for col in range(game.cols):
                line = [game.board[row + i, col] for i in range(4)]
                score += self._evaluate_line(line)

        for row in range(game.rows - 3):
            for col in range(game.cols - 3):
                line = [game.board[row + i, col + i] for i in range(4)]
                score += self._evaluate_line(line)

        for row in range(3, game.rows):
            for col in range(game.cols - 3):
                line = [game.board[row - i, col + i] for i in range(4)]
                score += self._evaluate_line(line)

        # Center preference
        center_col = game.cols // 2
        for row in range(game.rows):
            if game.board[row, center_col] == self.player_id:
                score += 2

        return score

    def _evaluate_line(self, line):
        """Evaluate a line of 4 positions for Connect Four or 3 for Tic Tac Toe"""
        my_pieces = line.count(self.player_id)
        opp_pieces = line.count(3 - self.player_id)
        empty_pieces = line.count(0)

        if my_pieces == len(line):  # Winning line
            return 100
        elif opp_pieces == len(line):  # Opponent winning line
            return -100
        elif opp_pieces == 0 and my_pieces > 0:  # Potential for me
            if my_pieces == len(line) - 1:  # One move from win
                return 10
            return my_pieces
        elif my_pieces == 0 and opp_pieces > 0:  # Potential for opponent
            if opp_pieces == len(line) - 1:  # One move from loss
                return -10
            return -opp_pieces
        return 0  # Blocked line