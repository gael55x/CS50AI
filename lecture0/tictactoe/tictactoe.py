"""
Tic Tac Toe Player
"""

import math

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
    # Initialize counter for X and O
    counterX = 0
    counterO = 0

    # Count how many X and O there are in the board
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == X:
                counterX += 1
            if board[row][column] == O:
                counterO += 1

    # If there are more X then O, next turn is O
    if counterX > counterO:
        return O
    # If there is O == X, next turn is X
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()  # Initialize an empty set to store possible actions

    for i in range(3):  # Iterate over rows
        for j in range(3):  # Iterate over columns
            if board[i][j] == EMPTY:  # Check if the cell is empty
                # If empty, add the action (i, j) to possible_actions
                possible_actions.add((i, j))

    return possible_actions  # Return the set of all possible actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):  # Check if the action is valid for the current board
        # Raise an exception if the action is not valid
        raise ValueError("Invalid action: Not a valid move!")

    # Create a new copy of the board to avoid modifying the original
    new_board = [row[:] for row in board]

    # Update the new board with the player's symbol based on the action (i, j)
    new_board[action[0]][action[1]] = player(board)

    # Return the new board that results from the action, representing the updated game state
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for symbol in [X, O]:
        # Check rows
        for row in board:
            if all(cell == symbol for cell in row):
                return symbol

        # Check columns
        for col in range(3):
            if all(row[col] == symbol for row in board):
                return symbol

        # Check diagonals
        # 1st diagonal: all(board[i][i] == symbol for i in range(3)):
            # If all elements along the main diagonal have the same value as the symbol,
            # it indicates that a player has achieved three-in-a-row along the main diagonal.
            # In this case, the function returns the symbol as the winner.
        # 2nd diagonal: all(board[i][2 - i] == symbol for i in range(3)):
            # If all elements along the anti-diagonal have the same value as the symbol,
            # it indicates that a player has achieved three-in-a-row along the anti-diagonal.
            # In this case, the function returns the symbol as the winner.
        if all(board[i][i] == symbol for i in range(3)) or all(board[i][2 - i] == symbol for i in range(3)):
            return symbol

    return None  # No winner found


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check if there's a winner
    if winner(board):
        return True

    # Check if the board is completely filled
    for row in board:
        if any(cell == EMPTY for cell in row):
            return False

    return True  # Game is over without a winner


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_symbol = winner(board)  # Get the symbol of the winner, if any
    if winner_symbol == X:
        return 1  # If X has won, return 1
    elif winner_symbol == O:
        return -1  # If O has won, return -1
    else:
        return 0  # If no winner, return 0 (game is a tie)


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):  # Check if the game is over
        return None  # If game is over, return None (no more moves can be made)

    current_player = player(board)  # Get the current player's symbol
    if current_player == X:
        # Find the maximum value action for X
        value, action = max_value(board, float('-inf'), float('inf'))
    else:
        # Find the minimum value action for O
        value, action = min_value(board, float('-inf'), float('inf'))

    return action  # Return the optimal action for the current player


def max_value(board, alpha, beta):
    if terminal(board):  # Check if the game is over
        # Return the utility value and no action if game is over
        return utility(board), None

    v = float('-inf')  # Initialize the value to negative infinity
    best_action = None  # Initialize the best action to None

    for action in actions(board):  # Iterate over possible actions
        # Get the new board after taking the action
        new_board = result(board, action)
        # Find the minimum value for the opponent
        min_val, _ = min_value(new_board, alpha, beta)
        if min_val > v:  # If opponent's value is greater than current value
            v = min_val  # Update the current value
            best_action = action  # Update the best action
        alpha = max(alpha, v)  # Update the alpha value
        if v >= beta:  # Prune the search if value is greater than or equal to beta
            break

    return v, best_action  # Return the maximum value and corresponding action


def min_value(board, alpha, beta):
    if terminal(board):  # Check if the game is over
        # Return the utility value and no action if game is over
        return utility(board), None

    v = float('inf')  # Initialize the value to positive infinity
    best_action = None  # Initialize the best action to None

    for action in actions(board):  # Iterate over possible actions
        # Get the new board after taking the action
        new_board = result(board, action)
        # Find the maximum value for the opponent
        max_val, _ = max_value(new_board, alpha, beta)
        if max_val < v:  # If opponent's value is smaller than current value
            v = max_val  # Update the current value
            best_action = action  # Update the best action
        beta = min(beta, v)  # Update the beta value
        if v <= alpha:  # Prune the search if value is less than or equal to alpha
            break

    return v, best_action  # Return the minimum value and corresponding action
