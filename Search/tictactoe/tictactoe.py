"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    X_count = 0
    O_count = 0

    for row in board:
        for cell in row:
            if cell == "X":
                X_count += 1
            elif cell == "O":
                O_count += 1

    if X_count == O_count:
        return X
    elif X_count > O_count:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    empty_cells = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                empty_cells.add((i, j))

    return empty_cells


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    if board[i][j] != EMPTY:
        raise Exception

    board_state = copy.deepcopy(board)
    board_state[i][j] = player(board)
    return board_state


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winning_combinations = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]
    ]

    for combination in winning_combinations:
        symbols = [board[i][j] for i, j in combination]
        if symbols[0] != EMPTY and all(symbol == symbols[0] for symbol in symbols):
            return symbols[0]
        
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) or all(board[i][j] != EMPTY for i in range(3) for j in range(3))


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    elif terminal(board):
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    if player(board) == X:
        for action in actions(board):
            if max_value(board) == min_value(result(board, action)):
                best_move = action
    elif player(board) == O:
        for action in actions(board):
            if min_value(board) == max_value(result(board, action)):
                best_move = action

    return best_move


def max_value(board):
    if terminal(board):
        return utility(board)

    v = float("-inf")
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    if terminal(board):
        return utility(board)

    v = float("inf")
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v