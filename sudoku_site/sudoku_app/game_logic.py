import math 
import random

board = []
for i in range(0,9):
    board.append([])
    for k  in range(0,9):
        board[i].append(0)

def isPresentInRow(num, row_num, board):
    return (num in board[row_num])

def isPresentInColumn(num,col_num,board):
    for row in range(0,9):
        if (board[row][col_num] == num):
            return True;
    return False

def isPresentInQuadrant(num, row_num, col_num, board):
    quad_x = math.floor( col_num / 3)
    quad_y = math.floor( row_num / 3)
    for row in range(0,9):
        for col  in range(0,9):
            quad_x_examined = math.floor( col / 3)
            quad_y_examined = math.floor( row / 3)
            if (quad_x_examined == quad_x) and\
               (quad_y_examined == quad_y) and\
               (board[row][col] == num):
                   return True;
    return False;

def isValidAllocation(num,row,col,board):
    if (isPresentInRow(num,row,board) or\
        isPresentInColumn(num,col,board) or\
        isPresentInQuadrant(num,row,col,board) or num ==0):
        return False
    else:
        return True

start_arr = [1,2,3,4,5,6,7,8,9]


number_of_hints = 25;
for hint in range(0,number_of_hints):
    row = random.randint(0,8)
    col = random.randint(0,8)
    while(board[row][col] != 0):
        row = random.randint(0,8)
        col = random.randint(0,8)
    possible_hint = 0
    while (isValidAllocation(possible_hint,row,col,board) == False):
        possible_hint = random.randint(1,9)
    board[row][col] = possible_hint



    
def SolveBoard(board_to_solve):
    for row in range(0,9):
        for col in range(0,9):
            if (board_to_solve[row][col] == 0):
                for num_to_try in range(1,10):
                    if (isValidAllocation(num_to_try,row,col,board_to_solve)):
                        board_to_solve[row][col] = num_to_try
                        if (SolveBoard(board_to_solve)):
                            return True
                        else:
                            board_to_solve[row][col] = 0
                return False    
    return True

SolveBoard(board)



test_board = []
for i in range(0,9):
    test_board.append([])
    for k  in range(0,9):
        test_board[i].append(0)
test_board[0][4] = 8


print(isPresentInRow(0, 3, test_board))
print(isPresentInRow(1, 3, test_board))
print(isPresentInRow(8, 0, test_board))
print(isPresentInColumn(0, 3, test_board))
print(isPresentInColumn(1, 3, test_board))
print(isPresentInQuadrant(1, 3, 3, test_board))
print(isPresentInQuadrant(8, 1, 5, test_board))
test_board[0][0] = 1
print(isPresentInColumn(1, 0, test_board))
print(isPresentInRow(1, 0, test_board))
print(isPresentInQuadrant(8, 1, 5, test_board))