import random

def print_board(board):
    for row in board:
        print(" | ".join(row))
    print("\n")

def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    
    return False

def get_available_moves(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]

def minimax(board, is_maximizing):
    if check_winner(board, "X"):
        return -1
    if check_winner(board, "O"):
        return 1
    if not get_available_moves(board):
        return 0
    
    if is_maximizing:
        best_score = -float("inf")
        for row, col in get_available_moves(board):
            board[row][col] = "O"
            score = minimax(board, False)
            board[row][col] = " "
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for row, col in get_available_moves(board):
            board[row][col] = "X"
            score = minimax(board, True)
            board[row][col] = " "
            best_score = min(score, best_score)
        return best_score

def best_move(board):
    best_score = -float("inf")
    move = None
    for row, col in get_available_moves(board):
        board[row][col] = "O"
        score = minimax(board, False)
        board[row][col] = " "
        if score > best_score:
            best_score = score
            move = (row, col)
    return move

def tic_tac_toe():
    board = [[" " for _ in range(3)] for _ in range(3)]
    print("Tic-Tac-Toe: You are 'X', AI is 'O'")
    print_board(board)
    
    while True:
        user_row, user_col = map(int, input("Enter your move (row and column: 0 1 2): ").split())
        if board[user_row][user_col] != " ":
            print("Invalid move, try again.")
            continue
        board[user_row][user_col] = "X"
        
        if check_winner(board, "X"):
            print_board(board)
            print("You win!")
            break
        
        if not get_available_moves(board):
            print_board(board)
            print("It's a tie!")
            break
        
        ai_row, ai_col = best_move(board)
        board[ai_row][ai_col] = "O"
        
        if check_winner(board, "O"):
            print_board(board)
            print("AI wins!")
            break
        
        print_board(board)

tic_tac_toe()
