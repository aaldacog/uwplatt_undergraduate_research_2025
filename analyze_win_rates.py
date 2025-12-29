#!/usr/bin/env python3
import os
import csv
import glob
import argparse
from collections import defaultdict


class WinRateAnalyzer:
    def __init__(self):
        self.all_results = []
        self.player_types = set()

    def load_data(self, game_type='ttt'):
        """Load all CSV files for a specific game type"""
        data_dir = os.path.join("data", game_type)

        if not os.path.exists(data_dir):
            print(f"Error: Data directory '{data_dir}' not found!")
            return False

        csv_files = glob.glob(os.path.join(data_dir, "game_results_*.csv"))

        if not csv_files:
            print(f"Error: No CSV files found in '{data_dir}'!")
            return False

        print(f"Found {len(csv_files)} CSV file(s) for {game_type}")

        total_games = 0
        for csv_file in csv_files:
            try:
                with open(csv_file, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        self.all_results.append(row)
                        self.player_types.add(row['first_player_type'])
                        self.player_types.add(row['second_player_type'])
                total_games += 1
                print(f"  Loaded {csv_file}")
            except Exception as e:
                print(f"  Error loading {csv_file}: {e}")

        print(f"Total games loaded: {len(self.all_results)}")
        print(f"Player types found: {sorted(self.player_types)}")
        return True

    def analyze_win_rates(self):
        """Calculate win rates between all player type combinations"""
        if not self.all_results:
            print("No data to analyze!")
            return

        # Dictionary to store matchup statistics
        # Format: matchup_stats[first_player_type][second_player_type] = {'wins': X, 'losses': Y, 'draws': Z, 'total': N}
        matchup_stats = defaultdict(lambda: defaultdict(lambda: {'wins': 0, 'losses': 0, 'draws': 0, 'total': 0}))

        for game in self.all_results:
            first_type = game['first_player_type']
            second_type = game['second_player_type']
            was_draw = game['was_draw'].lower() == 'true'

            stats = matchup_stats[first_type][second_type]
            stats['total'] += 1

            if was_draw:
                stats['draws'] += 1
            else:
                winner_type = game['winner_player_type']
                if winner_type == first_type:
                    stats['wins'] += 1
                else:
                    stats['losses'] += 1

        return matchup_stats

    def print_win_rate_table(self, matchup_stats):
        """Print a formatted win rate table"""
        if not matchup_stats:
            print("No matchup statistics to display!")
            return

        player_types = sorted(self.player_types)

        print("\n" + "=" * 80)
        print("WIN RATE ANALYSIS")
        print("=" * 80)
        print("X-axis: Player going first (row)")
        print("Y-axis: Player going second (column)")
        print("Values: Win rate of first player against second player")
        print("=" * 80)

        # Print header
        header = "First \\ Second" + " " * 5
        for second_type in player_types:
            header += f"{second_type:^12}"
        print(header)
        print("-" * (15 + len(player_types) * 12))

        # Print each row
        for first_type in player_types:
            row = f"{first_type:15}"
            for second_type in player_types:
                stats = matchup_stats[first_type][second_type]
                total = stats['total']

                if total == 0:
                    row += f"{'N/A':^12}"
                else:
                    win_rate = (stats['wins'] / total) * 100
                    row += f"{win_rate:>6.1f}% ({total:>4})"

            print(row)

        print("=" * 80)

    def print_detailed_statistics(self, matchup_stats):
        """Print detailed statistics for each matchup"""
        print("\n" + "=" * 80)
        print("DETAILED MATCHUP STATISTICS")
        print("=" * 80)

        player_types = sorted(self.player_types)

        for first_type in player_types:
            for second_type in player_types:
                stats = matchup_stats[first_type][second_type]
                total = stats['total']

                if total > 0:
                    win_rate = (stats['wins'] / total) * 100
                    loss_rate = (stats['losses'] / total) * 100
                    draw_rate = (stats['draws'] / total) * 100

                    print(f"\n{first_type} (First) vs {second_type} (Second):")
                    print(f"  Total games: {total}")
                    print(f"  First player wins: {stats['wins']} ({win_rate:.1f}%)")
                    print(f"  Second player wins: {stats['losses']} ({loss_rate:.1f}%)")
                    print(f"  Draws: {stats['draws']} ({draw_rate:.1f}%)")

        print("=" * 80)

    def save_results_to_csv(self, matchup_stats, game_type):
        """Save the analysis results to a CSV file"""
        output_dir = "analysis_results"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        timestamp = os.path.basename(glob.glob(os.path.join("data", game_type, "game_results_*.csv"))[0]).split('_')[
                    2:4]
        timestamp = '_'.join(timestamp).replace('.csv', '')

        filename = f"win_rates_{game_type}_{timestamp}.csv"
        filepath = os.path.join(output_dir, filename)

        player_types = sorted(self.player_types)

        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write header
            header = ['First_Player/Second_Player'] + list(player_types)
            writer.writerow(header)

            # Write data rows
            for first_type in player_types:
                row = [first_type]
                for second_type in player_types:
                    stats = matchup_stats[first_type][second_type]
                    total = stats['total']

                    if total == 0:
                        row.append('N/A')
                    else:
                        win_rate = (stats['wins'] / total) * 100
                        row.append(f"{win_rate:.1f}%")

                writer.writerow(row)

            # Write summary statistics
            writer.writerow([])
            writer.writerow(['Detailed Statistics:'])
            writer.writerow(
                ['First Player', 'Second Player', 'Total Games', 'First Wins', 'Second Wins', 'Draws', 'First Win %'])

            for first_type in player_types:
                for second_type in player_types:
                    stats = matchup_stats[first_type][second_type]
                    total = stats['total']

                    if total > 0:
                        win_rate = (stats['wins'] / total) * 100
                        writer.writerow([
                            first_type, second_type, total,
                            stats['wins'], stats['losses'], stats['draws'],
                            f"{win_rate:.1f}%"
                        ])

        print(f"\nAnalysis saved to: {filepath}")


def main():
    parser = argparse.ArgumentParser(description='Analyze win rates from simulation data')
    parser.add_argument('game_type',
                        choices=['tictactoe', 'connectfour', 'ttt', 'c4'],
                        default='ttt', nargs='?',
                        help='Type of game to analyze (default: ttt)')
    parser.add_argument('--detailed', action='store_true',
                        help='Show detailed matchup statistics')

    args = parser.parse_args()

    analyzer = WinRateAnalyzer()

    if analyzer.load_data(args.game_type):
        matchup_stats = analyzer.analyze_win_rates()

        if matchup_stats:
            analyzer.print_win_rate_table(matchup_stats)

            if args.detailed:
                analyzer.print_detailed_statistics(matchup_stats)

            analyzer.save_results_to_csv(matchup_stats, args.game_type)


if __name__ == "__main__":
    main()