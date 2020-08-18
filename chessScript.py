import chess
import random
import time
from IPython.display import display, HTML, clear_output
from string import ascii_lowercase
import numpy as np

board = chess.Board()
points_array = np.zeros((8,8)) # currently a dummy variable with no real meaning
depth = 5

def miniMaxTreeBuilder():
    every_legal_move_possible = list(board.legal_moves)
    bestVal = -10000
    bestMove
    for currMove in every_legal_move_possible:
        board.push_uci(currMove)
        currVal = miniMax(depth - 1, isMax)
        board.pop()
        if (currVal > bestVal):
            bestVal = currVal
            bestMove = currMove
    board.push_uci(bestMove)

def minimax(curr_depth, isMax):
    every_legal_move_possible = list(board.legal_moves)
    best_val_for_maximizing_player = -10000
    if (curr_depth == 0):
        return evaluate_board(board)
    if (isMax):
        for currMove in every_legal_move_possible:
            board.push_uci(currMove)
            best_val_for_maximizing_player = max(miniMax(depth - 1, not(isMax)),best_val_for_maximizing_player)
            board.pop()

        # do stuff here
    else:
        # do min stuff here



# This is a useful function to reverse the score arrays to be used for evaluation of board score
def reverse_points_array(score_array):
    return np.flip(score_array,axis=0)

# Currently, this function only prints out the kind of chess piece at every position on the board
def evaluate_board(board):
    board = chess.Board(board.fen())
    for (index,c) in enumerate(ascii_lowercase):
        if (c<='h'):
            for num in range(0,8):
                c = c.capitalize()
                points_array[index][num] = index
                chess_square = str(c)+str(num+1)
                print(chess_square+':',end ='')
                script = 'print(board.piece_at(chess.'+chess_square+'))'
                exec(script)
        else:
            break

def random_player(board):
    move = random.choice(list(board.legal_moves))
    return move.uci()

def who(player):
    return "White" if player == chess.WHITE else "Black"

def display_board(board, use_svg):
    if use_svg:
        return board._repr_svg_()
    else:
        return "<pre>" + str(board) + "</pre>"

def play_game(player1, player2, visual="svg", pause=0.1):
    """
    playerN1, player2: functions that takes board, return uci move
    visual: "simple" | "svg" | None
    """
    use_svg = (visual == "svg")
    board = chess.Board()
    try:
        while not board.is_game_over(claim_draw=True):
            if board.turn == chess.WHITE:
                uci = player1(board)
            else:
                uci = player2(board)
            name = who(board.turn)
            board.push_uci(uci)
            board_stop = display_board(board, use_svg)
            html = "<b>Move %s %s, Play '%s':</b><br/>%s" % (
                       len(board.move_stack), name, uci, board_stop)
            if visual is not None:
                if visual == "svg":
                    clear_output(wait=True)
                display(HTML(html))
                if visual == "svg":
                    time.sleep(pause)
    except KeyboardInterrupt:
        msg = "Game interrupted!"
        return (None, msg, board)
    result = None
    if board.is_checkmate():
        msg = "checkmate: " + who(not board.turn) + " wins!"
        result = not board.turn
    elif board.is_stalemate():
        msg = "draw: stalemate"
    elif board.is_fivefold_repetition():
        msg = "draw: 5-fold repetition"
    elif board.is_insufficient_material():
        msg = "draw: insufficient material"
    elif board.can_claim_draw():
        msg = "draw: claim"
    if visual is not None:
        print(msg)
    return (result, msg, board)

def human_player(board):
    display(board)
    uci = get_move("%s's move [q to quit]> " % who(board.turn))
    legal_uci_moves = [move.uci() for move in board.legal_moves]
    while uci not in legal_uci_moves:
        print("Legal moves: " + (",".join(sorted(legal_uci_moves))))
        uci = get_move("%s's move[q to quit]> " % who(board.turn))
    return uci
def get_move(prompt):
    uci = input(prompt)
    if uci and uci[0] == "q":
        raise KeyboardInterrupt()
    try:
        chess.Move.from_uci(uci)
    except:
        uci = None
    return uci

evaluate_board(board)
print(points_array)
miniMaxTreeBuilder()
play_game(human_player, random_player)