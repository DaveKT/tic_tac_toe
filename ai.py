from game import Board


def _opponent(player):
    return "O" if player == "X" else "X"


def _score(board, maximizing_player, depth):
    winner = board.winner()
    if winner == maximizing_player:
        return 10 - depth
    if winner is not None:
        return depth - 10
    return 0


def minimax(board, maximizing_player, depth=0):
    if board.is_game_over():
        return _score(board, maximizing_player, depth)

    is_max_turn = board.current_player == maximizing_player
    best = float("-inf") if is_max_turn else float("inf")
    for move in board.available_moves():
        child = board.copy()
        child.make_move(move)
        value = minimax(child, maximizing_player, depth + 1)
        best = max(best, value) if is_max_turn else min(best, value)
    return best


def best_move(board, player):
    if board.current_player != player:
        raise ValueError(
            f"It is {board.current_player}'s turn, not {player}'s."
        )
    moves = board.available_moves()
    if not moves:
        raise ValueError("No moves available.")

    best_value = float("-inf")
    best_index = moves[0]
    for move in moves:
        child = board.copy()
        child.make_move(move)
        value = minimax(child, player, depth=1)
        if value > best_value:
            best_value = value
            best_index = move
    return best_index
