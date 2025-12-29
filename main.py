#!/usr/bin/env python3
import argparse
import sys
import os
import csv
from datetime import datetime
import random

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from games.tic_tac_toe import TicTacToe
from games.connect_four import ConnectFour
from players.human_player import HumanPlayer
from players.random_player import RandomPlayer
from players.minimax_player import MinimaxPlayer
from players.quantum_player import QuantumPlayer
from players.astar_player import AStarPlayer


class GameSimulator:
    def __init__(self):
        self.results = []

    def create_game(self, game_type):
        game_map = {
            'tictactoe': TicTacToe,
            'connectfour': ConnectFour,
            'ttt': TicTacToe,  # Short alias
            'c4': ConnectFour  # Short alias
        }

        game_class = game_map.get(game_type.lower())
        if game_class:
            return game_class()
        else:
            raise ValueError(f"Unknown game type: {game_type}")

    def create_player(self, player_type, player_id, depth=None):
        player_map = {
            'human': HumanPlayer,
            'random': RandomPlayer,
            'minimax': MinimaxPlayer,
            'quantum': QuantumPlayer,
            'astar': AStarPlayer,
            # Short aliases
            'h': HumanPlayer,
            'r': RandomPlayer,
            'mm': MinimaxPlayer,
            'q': QuantumPlayer,
            'a': AStarPlayer
        }

        player_class = player_map.get(player_type.lower())
        if player_class:
            if player_class in [MinimaxPlayer, AStarPlayer]:
                if depth is None:
                    depth = 3  # Default depth
                return player_class(player_id, depth)
            else:
                # For non-depth players, we still track depth for CSV but set to -1
                return player_class(player_id)
        else:
            raise ValueError(f"Unknown player type: {player_type}")

    def play_game(self, game, player1, player2, show_graphics=True):
        players = {1: player1, 2: player2}

        if show_graphics:
            print(f"\nStarting new game: {player1} vs {player2}")
            print(game.display_board())

        while not game.game_over:
            current_player = players[game.current_player]
            move = current_player.get_move(game)

            if not game.make_move(move):
                print(f"Invalid move by {current_player}: {move}")
                continue

            if show_graphics:
                print(f"{current_player} played: {move}")
                print(game.display_board())

        # Determine result
        if game.winner == 0:
            result = "draw"
            winner = None
        else:
            result = "win"
            winner = players[game.winner]

        if show_graphics:
            if result == "draw":
                print("Game ended in a draw!")
            else:
                print(f"{winner} wins!")

        return result, winner

    def run_simulation(self, args):
        total_games = args.num_games
        wins_player1 = 0
        wins_player2 = 0
        draws = 0

        print(f"Starting simulation: {args.game_type}")
        print(f"Player 1: {args.player1_type} (Depth: {args.depth1})")
        print(f"Player 2: {args.player2_type} (Depth: {args.depth2})")
        print(f"Games: {total_games}")
        print(f"First player: {args.first_player}")

        for game_num in range(total_games):
            # Determine who goes first
            if args.first_player.lower()[0] == "r":
                first_player = random.choice([1, 2])
            else:
                first_player = int(args.first_player)

            # Create game and players
            game = self.create_game(args.game_type)

            # Assign players based on who goes first with their respective depths
            if first_player == 1:
                player1 = self.create_player(args.player1_type, 1, args.depth1)
                player2 = self.create_player(args.player2_type, 2, args.depth2)
                player1_depth = args.depth1
                player2_depth = args.depth2
                player1_type = args.player1_type
                player2_type = args.player2_type
            else:
                player1 = self.create_player(args.player2_type, 1, args.depth2)
                player2 = self.create_player(args.player1_type, 2, args.depth1)
                player1_depth = args.depth2
                player2_depth = args.depth1
                player1_type = args.player2_type
                player2_type = args.player1_type

            # Play the game
            result, winner = self.play_game(game, player1, player2, args.show_graphics)

            # Get winner info
            winner_type = None
            winner_depth = None
            if winner:
                if winner == player1:
                    winner_type = player1_type
                    winner_depth = player1_depth
                else:
                    winner_type = player2_type
                    winner_depth = player2_depth

            # Record results
            game_result = {
                'game_number': game_num + 1,
                'first_player': first_player,
                'player1_type': player1_type,
                'player2_type': player2_type,
                'player1_depth': player1_depth,
                'player2_depth': player2_depth,
                'result': result,
                'winner_type': winner_type,
                'winner_depth': winner_depth,
                'player1_went_first': (first_player == 1)
            }

            self.results.append(game_result)

            # Update statistics
            if result == "win":
                if winner == player1:
                    wins_player1 += 1
                else:
                    wins_player2 += 1
            else:
                draws += 1

            # if not args.show_graphics and (game_num + 1) % 10 == 0:
            #     print(f"Completed {game_num + 1}/{total_games} games...")

        # Print summary
        self.print_summary(wins_player1, wins_player2, draws, total_games)

        # Save results to CSV
        self.save_results(args)

    def print_summary(self, wins_player1, wins_player2, draws, total_games):
        print("\n" + "=" * 50)
        print("SIMULATION SUMMARY")
        print("=" * 50)
        print(f"Total games: {total_games}")
        print(f"Player 1 wins: {wins_player1} ({wins_player1 / total_games * 100:.1f}%)")
        print(f"Player 2 wins: {wins_player2} ({wins_player2 / total_games * 100:.1f}%)")
        print(f"Draws: {draws} ({draws / total_games * 100:.1f}%)")

        # Analyze first player advantage
        first_player_wins = 0
        second_player_wins = 0
        first_player_draws = 0

        for result in self.results:
            if result['result'] == 'win':
                if result['winner_type'] == result['player1_type'] and result['player1_went_first']:
                    first_player_wins += 1
                elif result['winner_type'] == result['player2_type'] and not result['player1_went_first']:
                    first_player_wins += 1
                else:
                    second_player_wins += 1
            else:
                first_player_draws += 1

        total_with_first = first_player_wins + second_player_wins + first_player_draws
        if total_with_first > 0:
            print(f"\nFirst player advantage:")
            print(f"First player wins: {first_player_wins} ({first_player_wins / total_with_first * 100:.1f}%)")
            print(f"Second player wins: {second_player_wins} ({second_player_wins / total_with_first * 100:.1f}%)")

    def save_results(self, args):
        # Create data directory for specific game type
        game_dir_map = {
            'tictactoe': 'ttt',
            'ttt': 'ttt',
            'connectfour': 'c4',
            'c4': 'c4'
        }
        game_subdir = game_dir_map.get(args.game_type.lower(), 'other')
        data_dir = os.path.join("data", game_subdir)

        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"game_results_{timestamp}.csv"
        filepath = os.path.join(data_dir, filename)

        with open(filepath, 'w', newline='') as csvfile:
            fieldnames = [
                'game_number',
                'first_player_number',
                'first_player_type',
                'first_player_depth',
                'second_player_number',
                'second_player_type',
                'second_player_depth',
                'winner_player_number',
                'winner_player_type',
                'winner_depth',
                'loser_player_number',
                'loser_player_type',
                'loser_depth',
                'was_draw'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for result in self.results:
                # Determine first and second player info
                if result['player1_went_first']:
                    first_player_number = 1
                    first_player_type = result['player1_type']
                    first_player_depth = result['player1_depth'] if first_player_type in ['minimax', 'astar', 'mm',
                                                                                          'a'] else -1

                    second_player_number = 2
                    second_player_type = result['player2_type']
                    second_player_depth = result['player2_depth'] if second_player_type in ['minimax', 'astar', 'mm',
                                                                                            'a'] else -1
                else:
                    first_player_number = 2
                    first_player_type = result['player2_type']
                    first_player_depth = result['player2_depth'] if first_player_type in ['minimax', 'astar', 'mm',
                                                                                          'a'] else -1

                    second_player_number = 1
                    second_player_type = result['player1_type']
                    second_player_depth = result['player1_depth'] if second_player_type in ['minimax', 'astar', 'mm',
                                                                                            'a'] else -1

                # Determine winner/loser info
                was_draw = result['result'] == 'draw'
                winner_player_number = None
                winner_player_type = None
                winner_depth = None
                loser_player_number = None
                loser_player_type = None
                loser_depth = None

                if not was_draw:
                    if result['winner_type'] == first_player_type:
                        winner_player_number = first_player_number
                        winner_player_type = first_player_type
                        winner_depth = first_player_depth if winner_player_type in ['minimax', 'astar', 'mm',
                                                                                    'a'] else -1

                        loser_player_number = second_player_number
                        loser_player_type = second_player_type
                        loser_depth = second_player_depth if loser_player_type in ['minimax', 'astar', 'mm',
                                                                                   'a'] else -1
                    else:
                        winner_player_number = second_player_number
                        winner_player_type = second_player_type
                        winner_depth = second_player_depth if winner_player_type in ['minimax', 'astar', 'mm',
                                                                                     'a'] else -1

                        loser_player_number = first_player_number
                        loser_player_type = first_player_type
                        loser_depth = first_player_depth if loser_player_type in ['minimax', 'astar', 'mm', 'a'] else -1

                # Write the detailed result
                row_data = {
                    'game_number': result['game_number'],
                    'first_player_number': first_player_number,
                    'first_player_type': first_player_type,
                    'first_player_depth': first_player_depth,
                    'second_player_number': second_player_number,
                    'second_player_type': second_player_type,
                    'second_player_depth': second_player_depth,
                    'winner_player_number': winner_player_number,
                    'winner_player_type': winner_player_type,
                    'winner_depth': winner_depth,
                    'loser_player_number': loser_player_number,
                    'loser_player_type': loser_player_type,
                    'loser_depth': loser_depth,
                    'was_draw': was_draw
                }
                writer.writerow(row_data)

        print(f"\nResults saved to: {filepath}")


def main():
    parser = argparse.ArgumentParser(description='Board Game Simulator')

    # Required arguments
    parser.add_argument('game_type',
                        choices=['tictactoe', 'connectfour', 'ttt', 'c4'],
                        help='Type of game to play (tictactoe/ttt, connectfour/c4)')
    parser.add_argument('player1_type',
                        choices=['human', 'random', 'minimax', 'quantum', 'astar', 'h', 'r', 'mm', 'q', 'a'],
                        help='Type of player 1 (human/h, random/r, minimax/mm, quantum/q, astar/a)')
    parser.add_argument('player2_type',
                        choices=['human', 'random', 'minimax', 'quantum', 'astar', 'h', 'r', 'mm', 'q', 'a'],
                        help='Type of player 2 (human/h, random/r, minimax/mm, quantum/q, astar/a)')

    # Optional arguments with short versions
    parser.add_argument('-f', '--first_player',
                        choices=['1', '2', 'random', 'r'], default='1',
                        help='Which player goes first (1, 2, random/r) (default: 1)')
    parser.add_argument('-g', '--num_games', type=int, default=1,
                        help='Number of games to play (default: 1)')
    parser.add_argument('-d1', '--depth1', type=int, default=3,
                        help='Depth for player 1 minimax and A* algorithms (default: 3)')
    parser.add_argument('-d2', '--depth2', type=int, default=3,
                        help='Depth for player 2 minimax and A* algorithms (default: 3)')
    parser.add_argument('-ng', '--no_graphics', action='store_true',
                        help='Turn off game graphics')

    args = parser.parse_args()

    # Set graphics flag
    args.show_graphics = not args.no_graphics

    # Create and run simulator
    simulator = GameSimulator()
    simulator.run_simulation(args)


if __name__ == "__main__":
    main()