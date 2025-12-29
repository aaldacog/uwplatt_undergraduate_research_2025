#!/usr/bin/env python3
import os
import sys
import argparse
from main import GameSimulator


class LargeSimulationRunner:
    def __init__(self):
        self.simulator = GameSimulator()
        self.all_player_types = ['random', 'minimax', 'quantum', 'astar']

    def run_large_simulations(self, game_type='ttt', games_per_matchup=10000):
        """Run large simulations with all player type combinations"""
        print(f"Starting LARGE simulations for {game_type.upper()}")
        print(f"Testing {len(self.all_player_types)} player types")
        print(f"{games_per_matchup:,} games per matchup")
        print(f"Total matchups: {len(self.all_player_types) ** 2}")
        print(f"Total games: {len(self.all_player_types) ** 2 * games_per_matchup:,}")
        print("=" * 60)

        matchup_count = 0
        total_matchups = len(self.all_player_types) ** 2

        for player1_type in self.all_player_types:
            for player2_type in self.all_player_types:
                matchup_count += 1
                print(f"\nMatchup {matchup_count}/{total_matchups}: {player1_type} vs {player2_type}")

                # Run with player1 going first
                print(f"  {player1_type} going first...")
                self._run_single_matchup(
                    game_type, player1_type, player2_type,
                    first_player='1', num_games=games_per_matchup
                )

                # Run with player2 going first
                print(f"  {player2_type} going first...")
                self._run_single_matchup(
                    game_type, player1_type, player2_type,
                    first_player='2', num_games=games_per_matchup
                )

        print(f"\nLARGE simulations completed!")

    def _run_single_matchup(self, game_type, player1_type, player2_type, first_player, num_games):
        """Run a single matchup configuration - results are automatically saved by GameSimulator"""

        # Create args object that will be passed to GameSimulator
        class Args:
            def __init__(self):
                self.game_type = game_type
                self.player1_type = player1_type
                self.player2_type = player2_type
                self.first_player = first_player
                self.num_games = num_games
                self.depth1 = 3  # Default depth for minimax/astar
                self.depth2 = 3  # Default depth for minimax/astar
                self.show_graphics = False
                self.no_graphics = True

        args = Args()

        # Run simulation - this will automatically save results to CSV
        self.simulator = GameSimulator()
        self.simulator.run_simulation(args)


def main():

    parser = argparse.ArgumentParser(description='Run large board game simulations')
    parser.add_argument('game_type',
                        choices=['tictactoe', 'connectfour', 'ttt', 'c4'],
                        default='ttt', nargs='?',
                        help='Type of game to simulate (default: ttt)')
    parser.add_argument('-g', '--games', type=int, default=10000,
                        help='Number of games per matchup (default: 10000)')

    args = parser.parse_args()

    runner = LargeSimulationRunner()
    runner.run_large_simulations(args.game_type, args.games)


if __name__ == "__main__":
    runs = 9
    while runs > 0:
        main()
        runs -= 1