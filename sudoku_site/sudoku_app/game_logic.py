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

def howManyTimesInRow(num, row_num, board):
    return (board[row_num].count(num))

def howManyTimesInColumn(num,col_num,board):
    how_many = 0
    for row in range(0,9):
        if (board[row][col_num] == num):
            how_many += 1
    return how_many

def howManyTimesInQuadrant(num, row_num, col_num, board):
    quad_x = math.floor( col_num / 3)
    quad_y = math.floor( row_num / 3)
    how_many = 0
    for row in range(0,9):
        for col  in range(0,9):
            quad_x_examined = math.floor( col / 3)
            quad_y_examined = math.floor( row / 3)
            if (quad_x_examined == quad_x) and\
               (quad_y_examined == quad_y) and\
               (board[row][col] == num):
                   how_many += 1
    return how_many;

def isValidAllocation(num,row,col,board):
    if (howManyTimesInRow(num,row,board) > 0 or\
        howManyTimesInColumn(num,col,board) > 0 or\
        howManyTimesInQuadrant(num,row,col,board) > 0 or num ==0):
        return False
    else:
        return True


def GetBoardWithHints(num_hints,deterministic_seed=0):
    board = CreateEmptyBoard();
    possible_hints = [1,2,3,4,5,6,7,8,9]
    for hint in range(0,num_hints):
        possible_row = [0,1,2,3,4,5,6,7,8]
        possible_col = [0,1,2,3,4,5,6,7,8]
        if (deterministic_seed == 0):
            random.shuffle(possible_row)
            random.shuffle(possible_col)
        else:
            random.Random(deterministic_seed).shuffle(possible_row)
            random.Random(deterministic_seed).shuffle(possible_col)
            
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
        
        if (deterministic_seed == 0):
            random.shuffle(possible_hints)
        else:
            random.Random(deterministic_seed).shuffle(possible_hints)
            
            
        for i in range(0,len(possible_hints)):
            if (isValidAllocation(possible_hints[i],good_row,good_col,board) == True):
                board[good_row][good_col] = possible_hints[i]
                break;

    return board

def checkHintBoard(board,expected_hints):
    
    generated_hints = 0 #counter
    for row in range (0,len(board)):
        for col in range(0,len(board[row])):
            hint = board[row][col]
            if  hint != 0:
                generated_hints = generated_hints +1 #count them  
                #check row
                if (howManyTimesInRow(hint,row,board) > 1): return False
                #check column
                if (howManyTimesInColumn(hint,col,board) > 1): return False
                #check quadrants
                if (howManyTimesInQuadrant(hint,row,col,board) > 1): return False
                
    if (generated_hints != expected_hints): return False
    
    return True
    
    
    
def checkSolution(board):
    
    for row in range (0,len(board)):
        for col in range(0,len(board[row])):
            to_check = board[row][col]
            if (to_check < 1): return False
            if (to_check > 9): return False
            
            if (howManyTimesInRow(to_check,row,board) != 1): return False            
            if (howManyTimesInColumn(to_check,col,board) != 1): return False
            if (howManyTimesInQuadrant(to_check,row,col,board) != 1): return False
            
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

def GetOneFullPuzzle(num_hints, deterministic_seed=0):
    ret = {
            "board_with_hints" : [],
            "solved_board" : []
          }
    board = GetBoardWithHints(num_hints, deterministic_seed)
    good_hb = checkHintBoard(board,num_hints)
    while(good_hb == False):
        board = GetBoardWithHints(num_hints)
        good_hb = checkHintBoard(board,num_hints)
        
    ret["board_with_hints"] = copy.deepcopy(board)
    sol = SolveBoard(board)
    while(sol==False):
        board = GetBoardWithHints(num_hints)
        ret["board_with_hints"] = copy.deepcopy(board)        
        sol = SolveBoard(board)
    ret["solved_board"] = board
    return ret

#puzzle = GetOneFullPuzzle(19)
#print(puzzle["board_with_hints"])
#print(puzzle["solved_board"])
#print(checkSolution(puzzle["solved_board"]))


