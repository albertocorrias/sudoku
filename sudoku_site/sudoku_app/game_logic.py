import math 
import random
import copy

def CreateEmptyBoard():
    board = []
    for i in range(0,9):
        board.append([])
        for k  in range(0,9):
            board[i].append(0)
    return board

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


def GetBoardWithHints(num_hints):
    board = CreateEmptyBoard();
    possible_hints = [1,2,3,4,5,6,7,8,9]
    for hint in range(0,num_hints):
        possible_row = [0,1,2,3,4,5,6,7,8]
        possible_col = [0,1,2,3,4,5,6,7,8]
        random.shuffle(possible_row)
        random.shuffle(possible_col)
        good_row = -1
        good_col = -1
        for row_idx in possible_row:
            if(good_row>-1):
                break;
            for col_idx in possible_col:
                if (board[row_idx][col_idx] == 0):
                    good_row = row_idx
                    good_col = col_idx
                    break;

        random.shuffle(possible_hints)
        for i in range(0,len(possible_hints)):
            if (isValidAllocation(possible_hints[i],good_row,good_col,board) == True):
                board[good_row][good_col] = possible_hints[i]
                break;

    return board

def checkSolution(board):
    numbers = [1,2,3,4,5,6,7,8,9]
    #check row
    for row in board:
        summation = sum(row)
        if (summation != sum(numbers)):
            return False
    #check columns
    sum_cols = 0
    for col in range(0,9):
        sum_cols=0
        for row in range(0,9):
            sum_cols = sum_cols + board[row][col]
        if (sum_cols != sum(numbers)):
            return False
    #check quadrants
    for row in range(0,9):
        quad_y = math.floor( row / 3)
        for col in range(0,9):
            quad_x = math.floor( col / 3)
            sum_quad=0
            for row_test in range(0,9):
                for col_test in range(0,9):
                    quad_x_examined = math.floor( col_test / 3)
                    quad_y_examined = math.floor( row_test / 3)
                    if (quad_x == quad_x_examined) and (quad_y == quad_y_examined):
                        sum_quad = sum_quad + board[row_test][col_test]
            if (sum_quad != sum(numbers)):
                return False
    return True
    
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

def GetOneFullPuzzle(num_hints):
    ret = {
            "board_with_hints" : [],
            "solved_board" : []
          }
    board = GetBoardWithHints(num_hints)
    ret["board_with_hints"] = copy.deepcopy(board)
    SolveBoard(board)
    ret["solved_board"] = board
    return ret

#puzzle = GetOneFullPuzzle(19)
#print(puzzle["board_with_hints"])
#print(puzzle["solved_board"])
#print(checkSolution(puzzle["solved_board"]))


