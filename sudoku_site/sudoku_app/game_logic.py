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

def countEmptyRows(board):
    ret = 0
    for row in range(0,9):
        if (sum(board[row])==0): ret += 1
    return ret;

def countEmptyColumns(board):
    not_empty = 0;
    for col in range(0,9):
        for row in range(0,9):
            if (board[row][col] != 0): 
                not_empty = not_empty + 1
                break;
    return 9 - not_empty;

def countEmptyQuadrants(board):
    ret = 0
    quad_rows = [0,3,6]
    quad_cols = [0,3,6]
    for row in quad_rows:
        for col in quad_cols:
            if (howManyTimesInQuadrant(0,row,col,board) == 9): ret = ret + 1
    return ret;

def AreHintsOnlyInRestrictedArea(board):
    '''
    See https://en.wikipedia.org/wiki/Mathematics_of_Sudoku
    Under "Constraints of clue geometry"

    This method returns True if the hints are NOT exclusively placed
    in the area that would make the puzzle unsolvable 
    '''
    if (sum(board[0][:])> 0): return False #First row not empty
    if (sum(board[8][:])> 0): return False #Last row not empty
    if (howManyTimesInColumn(0,0,board) < 9): return False #First Column not empty
    if (howManyTimesInColumn(0,8,board) < 9): return False #Last Column not empty
    if (board[4][4]> 0): return False #point in the middle not empty
    if (howManyTimesInQuadrant(0, 0, 0, board) < 9): return False #First quadrant not empty
    if (howManyTimesInQuadrant(0, 0, 8, board) < 9): return False #Top right quadrant not empty
    if (howManyTimesInQuadrant(0, 8, 0, board) < 9): return False #Bottom left quadrant not empty
    if (howManyTimesInQuadrant(0, 8, 8, board) < 9): return False #Bottom right quadrant not empty

    return True

def checkHintBoard(board,expected_hints):
    '''
    This methos checks for:
    1. Expected number of hints is there
    2. No repetition within row, column or quadrant
    3. "Solvability" of the puzzzle. This means that this method checks for
        the "Constraints of clue geometry" mentioned here https://en.wikipedia.org/wiki/Mathematics_of_Sudoku
        a) Number of empty groups must be < 9
        b) Largest rectangular "hole" < 30 squares
        c) "conjecture" of area where no proper puzzle should have hints only in that area
    '''    
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

    #Check number of hints            
    if (generated_hints != expected_hints): return False

    #Max 9 empty groups
    if (countEmptyRows(board) + countEmptyColumns(board) + countEmptyQuadrants(board) > 8):
        return False
    
    if AreHintsOnlyInRestrictedArea(board): return False
    
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




