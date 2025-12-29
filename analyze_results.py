#!/usr/bin/env python3
import os
import csv
import glob
from collections import defaultdict
import argparse


class ResultsAnalyzer:
    def __init__(self):
        self.all_results = []
        self.base_data_dir = "data"

    def load_all_csv_files(self, game_type):
        """Load all CSV files from the specific game type directory"""
        game_dir_map = {
            'tictactoe': 'ttt',
            'ttt': 'ttt',
            'connectfour': 'c4',
            'c4': 'c4'
        }

        game_subdir = game_dir_map.get(game_type.lower(), game_type.lower())
        data_dir = os.path.join(self.base_data_dir, game_subdir)

        if not os.path.exists(data_dir):
            print(f"Game directory '{data_dir}' not found!")
            return False

        csv_files = glob.glob(os.path.join(data_dir, "game_results_*.csv"))

        if not csv_files:
            print(f"No CSV files found in '{data_dir}' directory!")
            return False

        print(f"Found {len(csv_files)} CSV file(s) for {game_type}")

        for csv_file in csv_files:
            try:
                with open(csv_file, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        self.all_results.append(row)
                print(f"Loaded {os.path.basename(csv_file)}")
            except Exception as e:
                print(f"Error loading {csv_file}: {e}")

        print(f"Total {game_type} games loaded: {len(self.all_results)}")
        return True

    def analyze_matchups(self):
        """Analyze win/draw statistics for each player type matchup"""
        if not self.all_results:
            print("No data to analyze!")
            return {}

        # Filter out games with human players
        non_human_results = [
            r for r in self.all_results
            if r['player1_type'].lower() not in ['human', 'h']
               and r['player2_type'].lower() not in ['human', 'h']
        ]

        print(f"\nAnalyzing {len(non_human_results)} non-human games...")

        # Group by matchup
        matchups = defaultdict(lambda: {
            'total_games': 0,
            'player1_wins_first': 0,
            'player1_wins_second': 0,
            'player2_wins_first': 0,
            'player2_wins_second': 0,
            'draws_first': 0,
            'draws_second': 0,
            'player1_depths': set(),
            'player2_depths': set()
        })

        for game in non_human_results:
            # Create matchup key (sorted to avoid duplicates like A vs B and B vs A)
            player1_type = game['player1_type']
            player2_type = game['player2_type']
            player1_depth = game.get('player1_depth', 'N/A')
            player2_depth = game.get('player2_depth', 'N/A')

            matchup_key = tuple(sorted([f"{player1_type}(d{player1_depth})", f"{player2_type}(d{player2_depth})"]))

            # Update matchup statistics
            matchup = matchups[matchup_key]
            matchup['total_games'] += 1
            matchup['player1_depths'].add(player1_depth)
            matchup['player2_depths'].add(player2_depth)

            player1_went_first = game['player1_went_first'].lower() == 'true'
            result = game['result']
            winner_type = game.get('winner_type', '')

            if result == 'win':
                if winner_type == player1_type:
                    if player1_went_first:
                        matchup['player1_wins_first'] += 1
                    else:
                        matchup['player1_wins_second'] += 1
                else:  # winner_type == player2_type
                    if player1_went_first:
                        matchup['player2_wins_second'] += 1
                    else:
                        matchup['player2_wins_first'] += 1
            else:  # draw
                if player1_went_first:
                    matchup['draws_first'] += 1
                else:
                    matchup['draws_second'] += 1

        return matchups

    def print_detailed_analysis(self, matchups, game_type):
        """Print detailed analysis of all matchups"""
        print("\n" + "=" * 80)
        print(f"DETAILED MATCHUP ANALYSIS - {game_type.upper()}")
        print("=" * 80)

        for matchup_key, stats in sorted(matchups.items()):
            player1, player2 = matchup_key
            total_games = stats['total_games']

            print(f"\nMatchup: {player1} vs {player2}")
            print(f"Total games: {total_games}")
            print(f"Depths: {stats['player1_depths']} vs {stats['player2_depths']}")

            # Calculate percentages
            p1_wins_first = stats['player1_wins_first']
            p1_wins_second = stats['player1_wins_second']
            p2_wins_first = stats['player2_wins_first']
            p2_wins_second = stats['player2_wins_second']
            draws_first = stats['draws_first']
            draws_second = stats['draws_second']

            total_p1_wins = p1_wins_first + p1_wins_second
            total_p2_wins = p2_wins_first + p2_wins_second
            total_draws = draws_first + draws_second

            print(f"\nOverall Results:")
            print(f"  {player1} wins: {total_p1_wins} ({total_p1_wins / total_games * 100:.1f}%)")
            print(f"  {player2} wins: {total_p2_wins} ({total_p2_wins / total_games * 100:.1f}%)")
            print(f"  Draws: {total_draws} ({total_draws / total_games * 100:.1f}%)")

            print(f"\nWhen going FIRST:")
            first_total = p1_wins_first + p2_wins_first + draws_first
            if first_total > 0:
                print(f"  {player1} wins: {p1_wins_first} ({p1_wins_first / first_total * 100:.1f}%)")
                print(f"  {player2} wins: {p2_wins_first} ({p2_wins_first / first_total * 100:.1f}%)")
                print(f"  Draws: {draws_first} ({draws_first / first_total * 100:.1f}%)")

            print(f"\nWhen going SECOND:")
            second_total = p1_wins_second + p2_wins_second + draws_second
            if second_total > 0:
                print(f"  {player1} wins: {p1_wins_second} ({p1_wins_second / second_total * 100:.1f}%)")
                print(f"  {player2} wins: {p2_wins_second} ({p2_wins_second / second_total * 100:.1f}%)")
                print(f"  Draws: {draws_second} ({draws_second / second_total * 100:.1f}%)")

            # First player advantage
            first_player_wins = p1_wins_first + p2_wins_first
            second_player_wins = p1_wins_second + p2_wins_second
            total_wins = first_player_wins + second_player_wins

            if total_wins > 0:
                first_win_rate = first_player_wins / total_wins * 100
                print(f"\nFirst Player Win Rate: {first_win_rate:.1f}%")

    def print_summary_table(self, matchups, game_type):
        """Print a summary table of all matchups"""
        print("\n" + "=" * 100)
        print(f"SUMMARY TABLE - {game_type.upper()}")
        print("=" * 100)

        headers = ["Matchup", "Total", "P1 Wins", "P2 Wins", "Draws", "P1 Win%", "P2 Win%", "Draw%", "First Win%"]
        print(
            f"{headers[0]:<30} {headers[1]:>6} {headers[2]:>8} {headers[3]:>8} {headers[4]:>6} {headers[5]:>8} {headers[6]:>8} {headers[7]:>8} {headers[8]:>10}")
        print("-" * 100)

        for matchup_key, stats in sorted(matchups.items()):
            player1, player2 = matchup_key
            matchup_str = f"{player1} vs {player2}"

            total_games = stats['total_games']
            total_p1_wins = stats['player1_wins_first'] + stats['player1_wins_second']
            total_p2_wins = stats['player2_wins_first'] + stats['player2_wins_second']
            total_draws = stats['draws_first'] + stats['draws_second']

            p1_win_rate = total_p1_wins / total_games * 100 if total_games > 0 else 0
            p2_win_rate = total_p2_wins / total_games * 100 if total_games > 0 else 0
            draw_rate = total_draws / total_games * 100 if total_games > 0 else 0

            # First player win rate
            first_player_wins = stats['player1_wins_first'] + stats['player2_wins_first']
            total_wins = total_p1_wins + total_p2_wins
            first_win_rate = first_player_wins / total_wins * 100 if total_wins > 0 else 0

            print(f"{matchup_str:<30} {total_games:>6} {total_p1_wins:>8} {total_p2_wins:>8} {total_draws:>6} "
                  f"{p1_win_rate:>7.1f}% {p2_win_rate:>7.1f}% {draw_rate:>7.1f}% {first_win_rate:>9.1f}%")

    def save_analysis_to_csv(self, matchups, game_type):
        """Save the analysis results to a CSV file"""
        game_dir_map = {
            'tictactoe': 'ttt',
            'ttt': 'ttt',
            'connectfour': 'c4',
            'c4': 'c4'
        }

        game_subdir = game_dir_map.get(game_type.lower(), game_type.lower())
        data_dir = os.path.join(self.base_data_dir, game_subdir)

        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        output_file = os.path.join(data_dir, f"matchup_analysis_{game_type}.csv")

        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Player1', 'Player2', 'Total_Games', 'Player1_Wins', 'Player2_Wins', 'Draws',
                'Player1_Win_Rate', 'Player2_Win_Rate', 'Draw_Rate', 'First_Player_Win_Rate',
                'Player1_Wins_First', 'Player1_Wins_Second', 'Player2_Wins_First', 'Player2_Wins_Second',
                'Draws_First', 'Draws_Second'
            ])

            for matchup_key, stats in sorted(matchups.items()):
                player1, player2 = matchup_key

                total_games = stats['total_games']
                total_p1_wins = stats['player1_wins_first'] + stats['player1_wins_second']
                total_p2_wins = stats['player2_wins_first'] + stats['player2_wins_second']
                total_draws = stats['draws_first'] + stats['draws_second']

                p1_win_rate = total_p1_wins / total_games * 100 if total_games > 0 else 0
                p2_win_rate = total_p2_wins / total_games * 100 if total_games > 0 else 0
                draw_rate = total_draws / total_games * 100 if total_games > 0 else 0

                first_player_wins = stats['player1_wins_first'] + stats['player2_wins_first']
                total_wins = total_p1_wins + total_p2_wins
                first_win_rate = first_player_wins / total_wins * 100 if total_wins > 0 else 0

                writer.writerow([
                    player1, player2, total_games, total_p1_wins, total_p2_wins, total_draws,
                    f"{p1_win_rate:.1f}", f"{p2_win_rate:.1f}", f"{draw_rate:.1f}", f"{first_win_rate:.1f}",
                    stats['player1_wins_first'], stats['player1_wins_second'],
                    stats['player2_wins_first'], stats['player2_wins_second'],
                    stats['draws_first'], stats['draws_second']
                ])

        print(f"\nAnalysis saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Analyze game results by game type')
    parser.add_argument('game_type',
                        choices=['tictactoe', 'connectfour', 'ttt', 'c4'],
                        help='Type of game to analyze (tictactoe/ttt, connectfour/c4)')

    args = parser.parse_args()

    analyzer = ResultsAnalyzer()
    success = analyzer.load_all_csv_files(args.game_type)

    if success and analyzer.all_results:
        matchups = analyzer.analyze_matchups()
        analyzer.print_summary_table(matchups, args.game_type)
        analyzer.print_detailed_analysis(matchups, args.game_type)
        analyzer.save_analysis_to_csv(matchups, args.game_type)
    else:
        print(f"No data available for {args.game_type} analysis.")


if __name__ == "__main__":
    main()