from game import Board

_MAX_DEPTH = {"easy": 2, "hard": None}


def _opponent(player):
    return "O" if player == "X" else "X"


def _score(board, maximizing_player, depth):
    winner = board.winner()
    if winner == maximizing_player:
        return 10 - depth
    if winner is not None:
        return depth - 10
    return 0


def minimax(board, maximizing_player, depth=0, max_depth=None):
    if board.is_game_over():
        return _score(board, maximizing_player, depth)
    if max_depth is not None and depth >= max_depth:
        return 0

    is_max_turn = board.current_player == maximizing_player
    best = float("-inf") if is_max_turn else float("inf")
    for move in board.available_moves():
        child = board.copy()
        child.make_move(move)
        value = minimax(child, maximizing_player, depth + 1, max_depth)
        best = max(best, value) if is_max_turn else min(best, value)
    return best


def best_move(board, player, difficulty="hard"):
    if board.current_player != player:
        raise ValueError(
            f"It is {board.current_player}'s turn, not {player}'s."
        )
    moves = board.available_moves()
    if not moves:
        raise ValueError("No moves available.")

    max_depth = _MAX_DEPTH[difficulty]
    best_value = float("-inf")
    best_index = moves[0]
    for move in moves:
        child = board.copy()
        child.make_move(move)
        value = minimax(child, player, depth=1, max_depth=max_depth)
        if value > best_value:
            best_value = value
            best_index = move
    return best_index
