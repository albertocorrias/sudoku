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

def CalculateBoardSum(board):
    if (len(board)==0): return -1
    ret = 0
    for row in range(0,len(board)):
        for col in range(0,len(board[0])):
            ret += board[row][col]
    return ret

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

def isPresentInRow(num, row_num, board):
    '''
    Returns true is num is present in row_num of the board
    '''
    return (num in board[row_num])

def isPresentInColumn(num,col_num,board):
    '''
    Returns true is num is present in col_num of the board
    '''
    for row in range(0,9):
        if (board[row][col_num] == num):
            return True
    return False

# NOTE: These are hard-coded coordinates of each quadrant. It is not pretty,
# but these will be used by the check for presence in the quadrant,
# which, in turn, is called many times by the solver.
# Profiling revealed that hard-coding these values saves 
# 50% of the computation time
quad_0 = [[0,0],[0,1], [0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
quad_1 = [[0,3],[0,4], [0,5],[1,3],[1,4],[1,5],[2,3],[2,4],[2,5]]
quad_2 = [[0,6],[0,7], [0,8],[1,6],[1,7],[1,8],[2,6],[2,7],[2,8]]
quad_3 = [[3,0],[3,1], [3,2],[4,0],[4,1],[4,2],[5,0],[5,1],[5,2]]
quad_4 = [[3,3],[3,4], [3,5],[4,3],[4,4],[4,5],[5,3],[5,4],[5,5]]
quad_5 = [[3,6],[3,7], [3,8],[4,6],[4,7],[4,8],[5,6],[5,7],[5,8]]
quad_6 = [[6,0],[6,1], [6,2],[7,0],[7,1],[7,2],[8,0],[8,1],[8,2]]
quad_7 = [[6,3],[6,4], [6,5],[7,3],[7,4],[7,5],[8,3],[8,4],[8,5]]
quad_8 = [[6,6],[6,7], [6,8],[7,6],[7,7],[7,8],[8,6],[8,7],[8,8]]
quads = [quad_0, quad_1, quad_2, quad_3, quad_4, quad_5, quad_6, quad_7, quad_8]

def getQuadnumber(row,col):
    '''
    Method that returns the numbe rof the quadrant. It is not pretty,
    but avoding loops and hard-coding numbers showed to save a lot of time.
    '''
    if (row==0):
        if ((col==0) or (col==1) or (col==2)): return 0
        if ((col==3) or (col==4) or (col==5)): return 1
        if ((col==6) or (col==7) or (col==8)): return 2
    if (row==1):
        if ((col==0) or (col==1) or (col==2)): return 0
        if ((col==3) or (col==4) or (col==5)): return 1
        if ((col==6) or (col==7) or (col==8)): return 2
    if (row==2):
        if ((col==0) or (col==1) or (col==2)): return 0
        if ((col==3) or (col==4) or (col==5)): return 1
        if ((col==6) or (col==7) or (col==8)): return 2
    if (row==3):
        if ((col==0) or (col==1) or (col==2)): return 3
        if ((col==3) or (col==4) or (col==5)): return 4
        if ((col==6) or (col==7) or (col==8)): return 5
    if (row==4):
        if ((col==0) or (col==1) or (col==2)): return 3
        if ((col==3) or (col==4) or (col==5)): return 4
        if ((col==6) or (col==7) or (col==8)): return 5
    if (row==5):
        if ((col==0) or (col==1) or (col==2)): return 3
        if ((col==3) or (col==4) or (col==5)): return 4
        if ((col==6) or (col==7) or (col==8)): return 5
    if (row==6):
        if ((col==0) or (col==1) or (col==2)): return 6
        if ((col==3) or (col==4) or (col==5)): return 7
        if ((col==6) or (col==7) or (col==8)): return 8
    if (row==7):
        if ((col==0) or (col==1) or (col==2)): return 6
        if ((col==3) or (col==4) or (col==5)): return 7
        if ((col==6) or (col==7) or (col==8)): return 8
    if (row==8):
        if ((col==0) or (col==1) or (col==2)): return 6
        if ((col==3) or (col==4) or (col==5)): return 7
        if ((col==6) or (col==7) or (col==8)): return 8

def isPresentInQuadrant(num, row_num, col_num, board):
    '''
    Returns true if num is present in the same quadrant as
    position (row_num,col_num) in the board, false otherwise
    '''
    this_quad = getQuadnumber(row_num,col_num)
    to_be_examined = quads[this_quad];
    for cell in to_be_examined:
            row = cell[0]
            col = cell[1]
            if (board[row][col] == num):
                   return True;
    return False;

def isValidAllocation(num,row,col,board):
    '''
    Returns true if allocating num at position (row,col)
    of the board is OK for sudoku rules.
    '''
    if (isPresentInRow(num,row,board) == True or\
        isPresentInColumn(num,col,board) == True or\
        isPresentInQuadrant(num,row,col,board) == True or num ==0):
        return False
    else:
        return True

def GetBoardWithHints(num_hints,deterministic_seed=None):
    board = CreateEmptyBoard();
    possible_hints = [1,2,3,4,5,6,7,8,9]
    hints_successfully_placed  = 0
    random.seed(deterministic_seed)
    while(hints_successfully_placed  < num_hints):
        possible_position = random.randint(0,80)
        possible_row_idx = int(math.floor(possible_position/9))
        possible_col_idx = int(math.floor(possible_position%9))
        while (board[possible_row_idx][possible_col_idx] != 0):
            
            possible_position = random.randint(0,80)
            possible_row_idx = int(math.floor(possible_position/9))
            possible_col_idx = int(math.floor(possible_position%9))

        random.shuffle(possible_hints)
        
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

def IsThereEmpty30SquaresArea(board):
    return True;

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
        a) Number of empty groups must be <= 9
        b) "conjecture" of area where no proper puzzle should have hints only in that area

        Note that the other constraints (largest possible "hole" is 30 squares)
        is not checked here as the refrences provided are quite dubious and the solver
        should take care of it
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
    if (countEmptyRows(board) + countEmptyColumns(board) + countEmptyQuadrants(board) > 9):
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

def GetOneFullPuzzle(num_hints, deterministic_seed=None):
    ret = {
            "board_with_hints" : [],
            "solved_board" : []
          }
    board = GetBoardWithHints(num_hints, deterministic_seed)
    good_hb = checkHintBoard(board,num_hints)
    while(good_hb == False):
        board = GetBoardWithHints(num_hints, deterministic_seed)
        good_hb = checkHintBoard(board,num_hints)

    ret["board_with_hints"] = copy.deepcopy(board)
    sol = SolveBoard(board)
    while(sol==False):
        if (deterministic_seed != None): deterministic_seed += 1

        board = GetBoardWithHints(num_hints, deterministic_seed)
        ret["board_with_hints"] = copy.deepcopy(board)        
        sol = SolveBoard(board)
    ret["solved_board"] = board
    return ret
#helper method for testing purposes
def GetOneAlreadySolvedPuzzle():
    puzzle = GetOneFullPuzzle(32,1186)
    ret = {
            "board_with_hints" : [],
            "solved_board" : []
          }
    ret["board_with_hints"] = copy.deepcopy(puzzle["solved_board"])
    ret["solved_board"] = copy.deepcopy(puzzle["solved_board"])
    return ret

#another helper method for testing purposes
def GetOnePuzzliWithOneEmptyColumn():
    board = CreateEmptyBoard();
    ret = {
            "board_with_hints" : [],
            "solved_board" : []
    }

    board[0][0] = 9
    board[0][1] = 1
    board[0][2] = 2
    board[0][3] = 3
    board[0][4] = 4 
    #leave position 5 empty
    board[0][6] = 6
    board[0][7] = 7
    board[0][8] = 8
    
    ret["solved_board"] = copy.deepcopy(board)
    ret["board_with_hints"] = copy.deepcopy(board)
    return ret

    


