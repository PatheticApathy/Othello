import pygame
import sys
import numpy as np
import time

# constants
WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BOARD_COLOR = (128, 128, 128)

# global variables
states_examined = 0
player = -1
game_over = False
debug_mode = False
alpha_beta = True
depth = 2
computer_player = 1

# initialize pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello")

# game board
board = np.zeros((ROWS, COLS), dtype=int)
board[3, 3] = 1
board[4, 4] = 1
board[3, 4] = -1
board[4, 3] = -1

# function to make the board and pieces
def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(WIN, BOARD_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(WIN, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)

            piece = board[row, col]
            if piece != 0:
                color = WHITE if piece == 1 else BLACK
                pygame.draw.circle(WIN, color, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)

# function to check if your on the board
def on_board(x, y):
    return 0 <= x < ROWS and 0 <= y < COLS

# function to check if a move is valid
def valid_move(board, row, col, player):
    if board[row, col] != 0 or not on_board(row, col):
        return False
    opponent = -player
    directions = [(0, 1), (1, 0), (1, 1), (1, -1), (0, -1), (-1, 0), (-1, -1), (-1, 1)]
    for dx, dy in directions:
        x, y = row + dx, col + dy
        if on_board(x, y) and board[x, y] == opponent:
            while on_board(x, y) and board[x, y] == opponent:
                x, y = x + dx, y + dy
            if on_board(x, y) and board[x, y] == player:
                return True
    return False

# function to get valid moves
def get_valid_moves(board, player):
    valid_moves = []
    for row in range(ROWS):
        for col in range(COLS):
            if valid_move(board, row, col, player):
                valid_moves.append((row, col))
    return valid_moves

# function to flip pieces
def flip_pieces(board, row, col, player):
    opponent = -player
    directions = [(0, 1), (1, 0), (1, 1), (1, -1), (0, -1), (-1, 0), (-1, -1), (-1, 1)]
    board[row, col] = player
    for dx, dy in directions:
        x, y = row + dx, col + dy
        pieces_to_flip = []
        while on_board(x, y) and board[x, y] == opponent:
            pieces_to_flip.append((x, y))
            x, y = x + dx, y + dy
        if on_board(x, y) and board[x, y] == player:
            for px, py in pieces_to_flip:
                board[px, py] = player


# function to check if games over
def check_game_over():
    # game over if neither player has any valid moves
    if len(get_valid_moves(board, 1)) == 0 and len(get_valid_moves(board, -1)) == 0:
        return True
    return False

# function to get heuristics
def heuristic(board, player):
    # values for each position
    position_weights = np.array([
        [ 100, -10,  10,  10,  10,  10, -10, 100],
        [ -10, -50,  -2,  -2,  -2,  -2, -50, -10],
        [  10,  -2,   0,   0,   0,   0,  -2,  10],
        [  10,  -2,   0,   0,   0,   0,  -2,  10],
        [  10,  -2,   0,   0,   0,   0,  -2,  10],
        [  10,  -2,   0,   0,   0,   0,  -2,  10],
        [ -10, -50,  -2,  -2,  -2,  -2, -50, -10],
        [ 100, -10,  10,  10,  10,  10, -10, 100]
    ])
    
    # calculate the weighted score
    player_score = np.sum(position_weights * (board == player))
    opponent_score = np.sum(position_weights * (board == -player))
    return player_score - opponent_score

# function to perform the minimax algorithm
def minimax(board, depth, maximizing_player, alpha, beta, player, debug=False):
    global states_examined 
    # base case
    if depth == 0 or check_game_over():
        score = heuristic(board, player)
        if debug:
            print(f"Depth {depth}: Evaluating board -> Heuristic: {score}")
        return score, None
    
    valid_moves = get_valid_moves(board, player)
    # if there are no valid moves, evaluate board
    if not valid_moves:
        score = heuristic(board, player)
        if debug:
            print(f"Depth {depth}: No valid moves -> Heuristic: {score}")
        return score, None  # No valid moves, evaluate board
    
    best_move = None
    if maximizing_player:
        max_eval = float('-inf')
        for move in valid_moves:
            states_examined += 1
            new_board = board.copy()
            flip_pieces(new_board, move[0], move[1], player)
            if debug:
                print(f"Depth {depth}: Maximizing, Evaluating move {move}")
                print(new_board)
            eval_score, _ = minimax(new_board, depth - 1, False, alpha, beta, -player, debug)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            if alpha_beta:
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    if debug:
                        print(f"Pruning branch at move {move} with alpha {alpha} and beta {beta}")
                    break
        if debug:
            print(f"Best maximizing move at Depth {depth}: {best_move} with score {max_eval}")
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in valid_moves:
            states_examined += 1
            new_board = board.copy()
            flip_pieces(new_board, move[0], move[1], player)
            if debug:
                print(f"Depth {depth}: Minimizing, Evaluating move {move}")
                print(new_board)
            eval_score, _ = minimax(new_board, depth - 1, True, alpha, beta, -player, debug)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            if alpha_beta:
                beta = min(beta, eval_score)
                if beta <= alpha:
                    if debug:
                        print(f"Pruning branch at move {move} with alpha {alpha} and beta {beta}")
                    break
        if debug:
            print(f"Best minimizing move at Depth {depth}: {best_move} with score {min_eval}")
        return min_eval, best_move

# function to restart the game
def restart_game():
    global board, player, game_over
    board = np.zeros((ROWS, COLS), dtype=int)
    board[3, 3] = 1
    board[4, 4] = 1
    board[3, 4] = -1
    board[4, 3] = -1
    player = -1
    game_over = False

    WIN.fill(BOARD_COLOR)
    draw_board()
    pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    global player, game_over, debug_mode, depth, computer_player, states_examined, alpha_beta

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # get player's input
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
                if valid_move(board, row, col, player):
                    flip_pieces(board, row, col, player)
                    player = -player if len(get_valid_moves(board, -player)) > 0 else player
                    game_over = check_game_over()

            # computer's turn
            if player == computer_player and not game_over:
                if event.type == pygame.KEYDOWN:
                    # press "g" to start the computer's turn
                    if event.key == pygame.K_g:
                        # reset states_examined each turn
                        states_examined = 0
                        start = time.time()
                        _, best_move = minimax(board, depth, True, float('-inf'), float('inf'), player, debug=debug_mode)
                        end = time.time()
                        print(f"States examined: {states_examined}\nTime elapsed: {end - start}")
                        if best_move:
                            flip_pieces(board, best_move[0], best_move[1], player)
                            player = -player if len(get_valid_moves(board, -player)) > 0 else player
                            game_over = check_game_over()
            
            if event.type == pygame.KEYDOWN:
                # press "b" to toggle debug mode
                if event.key == pygame.K_b:
                    debug_mode = not debug_mode
                    print(f"Debug Mode: {'ON' if debug_mode else 'OFF'}")
                # press "a" to toggle alpha-beta pruning
                elif event.key == pygame.K_a:
                    alpha_beta = not alpha_beta
                    print(f"Alpha-Beta Pruning: {'ON' if alpha_beta else 'OFF'}")
                # press "r" to restart the game
                elif event.key == pygame.K_d:  # change depth
                    depth = int(input("Input depth: "))
                # press "r" to restart the game
                elif event.key == pygame.K_c:
                    computer_player = -computer_player
                # press "r" to restart the game
                elif event.key == pygame.K_r:
                    restart_game()

        draw_board()

        # print the game over message with the winner and score
        if game_over:
            font = pygame.font.SysFont("Arial", 50)
            white_count = np.sum(board == 1)
            black_count = np.sum(board == -1)
            winner = "White" if white_count > black_count else "Black" if black_count > white_count else "Draw"
            game_over_text = font.render("Game Over!", True, (255, 0, 0))
            winner_text = font.render(f"Winner: {winner}", True, (255, 0, 0))
            score_text = font.render(f"Black: {black_count}  White: {white_count}", True, (255, 0, 0))
            textpos1 = WIDTH // 2 - game_over_text.get_width() // 2, (HEIGHT // 2 - game_over_text.get_height() // 2) - 50
            textpos2 = WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2
            textpos3 = WIDTH // 2 - score_text.get_width() // 2, (HEIGHT // 2 - score_text.get_height() // 2) + 50
            WIN.blit(game_over_text, textpos1)
            WIN.blit(winner_text, textpos2)
            WIN.blit(score_text, textpos3)

        pygame.display.flip()
        clock.tick(60)

main()