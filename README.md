# Othello

## Overview
The `OthelloGame` program is a Python-based implementation of the classic Othello board game using Pygame. It supports human vs. human and human vs. AI gameplay, featuring a minimax algorithm with optional alpha-beta pruning for AI decision-making.

## Features
- Interactive GUI using Pygame.
- Supports two-player and AI gameplay modes.
- AI decision-making with the Minimax algorithm and optional alpha-beta pruning.
- Adjustable difficulty through depth selection.
- Debug mode for visualizing AI decision-making.
- Real-time score display and game-over detection.

## Game Rules
- Players take turns placing their pieces (Black or White) on the 8x8 board.
- A valid move must sandwich opponent pieces between the placed piece and another piece of the same color.
- The game ends when neither player can make a valid move.
- The player with the most pieces on the board at the end wins.

## Program Execution
Upon launching the program, players can:
1. Click on the board to place a piece.
2. Press `G` to allow the AI to make a move.
3. Toggle debugging (`B` key) and alpha-beta pruning (`A` key).
4. Adjust AI difficulty (`D` key) and switch AI color (`C` key).
5. Restart the game (`R` key).
6. Exit by closing the window.

## Core Functions
### `draw_board()`
Renders the game board and pieces.

### `valid_move(board, row, col, player)`
Checks if a move is valid for a given player.

### `get_valid_moves(board, player)`
Returns a list of all valid moves for a player.

### `flip_pieces(board, row, col, player)`
Flips opponent pieces after a valid move.

### `check_game_over()`
Determines if the game has ended.

### `heuristic(board, player)`
Evaluates the board state for AI decision-making.

### `minimax(board, depth, maximizing_player, alpha, beta, player, debug)`
AI decision-making algorithm using Minimax with optional alpha-beta pruning.

### `restart_game()`
Resets the board and game state.

## AI Gameplay
- The AI selects moves using Minimax, evaluating board positions based on predefined weights.
- Alpha-beta pruning can be enabled to optimize search efficiency.
- AI difficulty can be adjusted by changing the search depth.

## Controls
- `Left Click`: Place a piece.
- `G`: AI move.
- `B`: Toggle debug mode.
- `A`: Toggle alpha-beta pruning.
- `D`: Change AI depth.
- `C`: Switch AI color.
- `R`: Restart game.
- `Close Window`: Exit.

## Dependencies
- `pygame`
- `numpy`
- `sys`
- `time`

## Usage Example
```sh
python othello.py
```
