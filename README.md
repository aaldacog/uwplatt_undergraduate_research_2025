# Board Game Simulator

A modular Python program for simulating board games between different types of AI and human players. Supports Tic Tac Toe and Connect Four with various player algorithms including Minimax, A*, Quantum Random, and more.

## Quick Start

### Basic Single Game
```bash
# Human vs Minimax AI in Tic Tac Toe
python main.py tictactoe human minimax

# Human vs Random AI in Connect Four  
python main.py connectfour human random
```

### Tournament Simulations
```bash
# 100 games between Minimax and Random players
python main.py ttt minimax random -g 100 -ng

# 50 games between A* and Quantum players with random first player
python main.py c4 astar quantum -g 50 -f random -ng
```

## Game Types
- `tictactoe` or `ttt` - Tic Tac Toe (3x3 grid)
- `connectfour` or `c4` - Connect Four (6x7 grid)

## Player Types
- `human` or `h` - Human player (requires input)
- `random` or `r` - Random move selection
- `minimax` or `mm` - Minimax algorithm with alpha-beta pruning
- `astar` or `a` - A* search algorithm
- `quantum` or `q` - Quantum random moves using Qiskit

## Command Line Arguments

### Required Arguments
- `game_type` - Type of game (`tictactoe`, `connectfour`, `ttt`, `c4`)
- `player1_type` - Type of player 1 (`human`, `random`, `minimax`, `astar`, `quantum`)
- `player2_type` - Type of player 2 (`human`, `random`, `minimax`, `astar`, `quantum`)

### Optional Arguments
- `-f, --first_player` - Who goes first (`1`, `2`, `random`, `r`) [default: 1]
- `-g, --num_games` - Number of games to play [default: 1]
- `-d1, --depth1` - Search depth for player 1 (Minimax/A* only) [default: 3]
- `-d2, --depth2` - Search depth for player 2 (Minimax/A* only) [default: 3]
- `-ng, --no_graphics` - Turn off ASCII game display

## Examples

### Human vs AI Games
```bash
# Play Tic Tac Toe against Minimax AI (depth 4)
python main.py ttt human minimax -d2 4

# Play Connect Four against A* AI (depth 5)
python main.py c4 human astar -d2 5
```

### AI vs AI Tournaments
```bash
# Minimax (depth 3) vs Minimax (depth 5) - 100 games
python main.py ttt minimax minimax -g 100 -d1 3 -d2 5 -ng

# A* vs Quantum with random first player
python main.py c4 astar quantum -g 50 -f random -d1 4 -ng

# Compare different algorithms
python main.py ttt minimax astar -g 200 -d1 4 -d2 4 -ng
```

### Quick Short Command Examples
```bash
# Short commands for quick testing
python main.py ttt h mm          # Human vs Minimax
python main.py c4 r q -g 10 -ng  # Random vs Quantum, 10 games, no graphics
python main.py ttt mm a -d1 5    # Minimax (depth 5) vs A* (depth 3)
```

## Output

- **Console Results**: Win/loss statistics and game summaries
- **CSV Files**: Detailed results saved in `data/ttt/` or `data/c4/` directories
- **Game Display**: ASCII graphics showing board state (disable with `-ng`)

## Analysis

After running simulations, analyze the results:
```bash
# Analyze Tic Tac Toe results
python analyze_results.py ttt

# Analyze Connect Four results
python analyze_results.py c4
```

The analysis script provides:
- Win rates for each player type
- Performance when going first vs second
- First player advantage statistics
- Detailed matchup analysis

## Requirements

```bash
pip install numpy q.py
```

## Notes

- For human players, follow the prompts to input moves
- Higher depth values improve AI performance but increase computation time
- Quantum player requires Qiskit installation, falls back to classical random if unavailable
- Results are automatically organized by game type in the `data/` directory