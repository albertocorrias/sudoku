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


def GetBoardWithHints(num_hints,deterministic_seed=None):
    board = CreateEmptyBoard();
    possible_hints = [1,2,3,4,5,6,7,8,9]
    hints_successfully_placed  = 0
    while(hints_successfully_placed  < num_hints):
        possible_position = random.Random(deterministic_seed).randint(0,80)
        possible_row_idx = int(math.floor(possible_position/9))
        possible_col_idx = int(math.floor(possible_position%9))
        while (board[possible_row_idx][possible_col_idx] != 0):
            possible_position = random.randint(0,80)
            possible_row_idx = int(math.floor(possible_position/9))
            possible_col_idx = int(math.floor(possible_position%9))

        random.Random(deterministic_seed).shuffle(possible_hints)
        
        for i in range(0,len(possible_hints)):
            if (isValidAllocation(possible_hints[i],possible_row_idx,possible_col_idx,board) == True):
                board[possible_row_idx][possible_col_idx] = possible_hints[i]
                hints_successfully_placed  = hints_successfully_placed + 1
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
            "solved_board" : [],
            "seed_at_end" : 0
          }
    board = GetBoardWithHints(num_hints, deterministic_seed)
    good_hb = checkHintBoard(board,num_hints)
    while(good_hb == False):
        deterministic_seed += 1 
        board = GetBoardWithHints(num_hints, deterministic_seed)
        good_hb = checkHintBoard(board,num_hints)

    ret["board_with_hints"] = copy.deepcopy(board)
    sol = SolveBoard(board)
    while(sol==False):
        deterministic_seed += 1
        board = GetBoardWithHints(num_hints, deterministic_seed)
        ret["board_with_hints"] = copy.deepcopy(board)        
        sol = SolveBoard(board)
    ret["solved_board"] = board
    ret["seed_at_end"] = deterministic_seed
    return ret



