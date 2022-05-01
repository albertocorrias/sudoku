from django.test import TestCase
from django.urls import reverse
from decimal import *
from sudoku_app.game_logic import GetOneFullPuzzle,GetBoardWithHints,\
isValidAllocation,howManyTimesInQuadrant,howManyTimesInRow,howManyTimesInColumn,\
CreateEmptyBoard, SolveBoard,checkSolution, checkHintBoard, countEmptyRows, \
countEmptyColumns,countEmptyQuadrants,AreHintsOnlyInRestrictedArea,CalculateBoardSum, \
IsThereEmpty30SquaresArea

def CreateExampleTestBoard():
    tb = CreateEmptyBoard();
    #set it up like in the solver's video
    # 7 0 2 | 0 5 0 | 6 0 0
    # 0 0 0 | 0 0 3 | 0 0 0
    # 1 0 0 | 0 0 9 | 5 0 0
    # ---------------------
    # 8 0 0 | 0 0 0 | 0 9 0
    # 0 4 3 | 0 0 0 | 7 5 0
    # 0 9 0 | 0 0 0 | 0 0 8
    # ---------------------
    # 0 0 9 | 7 0 0 | 0 0 5
    # 0 0 0 | 2 0 0 | 0 0 0
    # 0 0 7 | 0 4 0 | 2 0 3 
    tb[0][0] = 7
    tb[0][2] = 2
    tb[0][4] = 5
    tb[0][6] = 6
    tb[1][5] = 3
    tb[2][0] = 1
    tb[2][5] = 9
    tb[2][6] = 5
    tb[3][0] = 8
    tb[3][7] = 9
    tb[4][1] = 4
    tb[4][2] = 3
    tb[4][6] = 7
    tb[4][7] = 5
    tb[5][1] = 9
    tb[5][8] = 8
    tb[6][2] = 9
    tb[6][3] = 7
    tb[6][8] = 5
    tb[7][3] = 2
    tb[8][2] = 7
    tb[8][4] = 4
    tb[8][6] = 2
    tb[8][8] = 3
    return tb

class TestGameLogic(TestCase):
    
    def test_create_empty_board(self):
        tb = CreateEmptyBoard();
        self.assertEqual(len(tb),9)
        for i in range(0,len(tb)):
            self.assertEqual(len(tb[i]),9)
            for k in range(0,len(tb[i])):
                self.assertEqual(tb[i][k],0)

    def test_sum_of_board(self):
        tb = CreateEmptyBoard();
        self.assertEqual(CalculateBoardSum(tb),0)
        tb[4][4] = 8
        self.assertEqual(CalculateBoardSum(tb),8)
        tb[7][7] = 9
        self.assertEqual(CalculateBoardSum(tb),8+9)
        #Try smaller board
        smaller = [[1,2],[3,4]]
        self.assertEqual(CalculateBoardSum(smaller),1+2+3+4)
        #try empty board for coverage
        empty = []
        self.assertEqual(CalculateBoardSum(empty),-1)

    def test_same_row(self):
        tb = CreateEmptyBoard();
        num = 2
        row_idx = 3
        col_idx = 4
        tb[row_idx][col_idx] = num
        for row in range(0,8):
            for num_to_try in range(1,9):
                if (num_to_try == num):
                    if (row==row_idx):
                        self.assertEqual(howManyTimesInRow(num_to_try,row,tb),1)
                    else:
                        self.assertEqual(howManyTimesInRow(num_to_try,row,tb),0)
                else:
                    self.assertEqual(howManyTimesInRow(num_to_try,row,tb),0)
                    
    def test_same_col(self):
        tb = CreateEmptyBoard();
        num = 2
        row_idx = 3
        col_idx = 4
        tb[row_idx][col_idx] = num
        for col in range(0,8):
            for num_to_try in range(1,9):
                if (num_to_try == num):
                    if (col==col_idx):
                        self.assertEqual(howManyTimesInColumn(num_to_try,col,tb),1)
                    else:
                        self.assertEqual(howManyTimesInColumn(num_to_try,col,tb),0)
                else:
                    self.assertEqual(howManyTimesInColumn(num_to_try,col,tb),0)
                        
                
    def test_same_quadrant(self):
        tb = CreateEmptyBoard();
        num = 2
        row_idx = 3
        col_idx = 2
        tb[row_idx][col_idx] = num
        
        quad_rows = [3,4,5]
        quad_cols = [0,1,2]
        for row in range(0,8):
            for col in range(0,8):
                for num_to_try in range(1,9):
                    if (num_to_try == num):
                        if (row in quad_rows) and (col in quad_cols):
                            self.assertEqual(howManyTimesInQuadrant(num_to_try,row,col,tb),1)
                        else:
                            self.assertEqual(howManyTimesInQuadrant(num_to_try,row,col,tb),0)
                    else:
                        self.assertEqual(howManyTimesInQuadrant(num_to_try,row,col,tb),0)
                    
    def test_same_quadrant_2(self):
        tb = CreateEmptyBoard();
        num = 2
        row_idx = 8
        col_idx = 8
        tb[row_idx][col_idx] = num
        
        quad_rows = [6,7,8]
        quad_cols = [6,7,8]
        for row in range(0,8):
            for col in range(0,8):
                for num_to_try in range(1,9):
                    if (num_to_try == num):
                        if (row in quad_rows) and (col in quad_cols):
                            self.assertEqual(howManyTimesInQuadrant(num_to_try,row,col,tb),1)
                        else:
                            self.assertEqual(howManyTimesInQuadrant(num_to_try,row,col,tb),0)
                    else:
                        self.assertEqual(howManyTimesInQuadrant(num_to_try,row,col,tb),0)         
    
    def test_is_valid_allocation(self):
        tb = CreateEmptyBoard();
        num = 2
        row_idx = 3
        col_idx = 2
        tb[row_idx][col_idx] = num
        
        quad_rows = [3,4,5]
        quad_cols = [0,1,2]
        for row in range(0,8):
            for col in range(0,8):
                for num_to_try in range(1,9):
                    if (num_to_try == num):
                        if ((row in quad_rows) and (col in quad_cols)) or \
                            (row==row_idx) or (col==col_idx):
                            self.assertEqual(isValidAllocation(num_to_try,row,col,tb),False)
                        else:
                            self.assertEqual(isValidAllocation(num_to_try,row,col,tb),True)
                    else:
                        self.assertEqual(isValidAllocation(num_to_try,row,col,tb),True)  

    def test_empty_counters(self):
        tb = CreateEmptyBoard();
        self.assertEqual(countEmptyRows(tb),9)
        self.assertEqual(countEmptyColumns(tb),9)
        self.assertEqual(countEmptyQuadrants(tb),9)

        tb[0][0] = 3
        self.assertEqual(countEmptyRows(tb),8)
        self.assertEqual(countEmptyColumns(tb),8)
        self.assertEqual(countEmptyQuadrants(tb),8)

        tb[8][8] = 5
        self.assertEqual(countEmptyRows(tb),7)
        self.assertEqual(countEmptyColumns(tb),7)
        self.assertEqual(countEmptyQuadrants(tb),7)

        tb[0][1] = 6
        self.assertEqual(countEmptyRows(tb),7)
        self.assertEqual(countEmptyColumns(tb),6)
        self.assertEqual(countEmptyQuadrants(tb),7)

        tb[4][0] = 9
        self.assertEqual(countEmptyRows(tb),6)
        self.assertEqual(countEmptyColumns(tb),6)
        self.assertEqual(countEmptyQuadrants(tb),6)

        tb[8][0] = 1
        self.assertEqual(countEmptyRows(tb),6)
        self.assertEqual(countEmptyColumns(tb),6)
        self.assertEqual(countEmptyQuadrants(tb),5)

        tb[1][1] = 4
        self.assertEqual(countEmptyRows(tb),5)
        self.assertEqual(countEmptyColumns(tb),6)
        self.assertEqual(countEmptyQuadrants(tb),5)

        new_tb = CreateExampleTestBoard()
        self.assertEqual(countEmptyRows(new_tb),0)
        self.assertEqual(countEmptyColumns(new_tb),0)
        self.assertEqual(countEmptyQuadrants(new_tb),1)

    def test_hints_in_restriced_area_only(self):
        tb = CreateEmptyBoard();
        self.assertEqual(AreHintsOnlyInRestrictedArea(tb),True)
        tb[4][1] = 8 
        self.assertEqual(AreHintsOnlyInRestrictedArea(tb),True)
        tb[7][4] = 8 
        self.assertEqual(AreHintsOnlyInRestrictedArea(tb),True)

        #Place one in first row
        tb[0][4] = 8 
        self.assertEqual(AreHintsOnlyInRestrictedArea(tb),False)
        #put it back
        tb[0][4] = 0
        self.assertEqual(AreHintsOnlyInRestrictedArea(tb),True)

        #Place one in last row
        tb[8][4] = 8 
        self.assertEqual(AreHintsOnlyInRestrictedArea(tb),False)
        #put it back
        tb[8][4] = 0
        self.assertEqual(AreHintsOnlyInRestrictedArea(tb),True)
        
        #Place one in first column
        tb[4][0] = 8 
        self.assertEqual(AreHintsOnlyInRestrictedArea(tb),False)
        #put it back
        tb[4][0] = 0
        self.assertEqual(AreHintsOnlyInRestrictedArea(tb),True)

        #Place one in last column
        tb[4][8] = 8 
        self.assertEqual(AreHintsOnlyInRestrictedArea(tb),False)
        #put it back
        tb[4][8] = 0
        self.assertEqual(AreHintsOnlyInRestrictedArea(tb),True)
        
        #Place one in the middle
        tb[4][4] = 8 
        self.assertEqual(AreHintsOnlyInRestrictedArea(tb),False)
        #put it back
        tb[4][4] = 0
        self.assertEqual(AreHintsOnlyInRestrictedArea(tb),True)

        #Place one in first quadrant
        tb[1][1] = 8 
        self.assertEqual(AreHintsOnlyInRestrictedArea(tb),False)
        #put it back
        tb[1][1] = 0
        self.assertEqual(AreHintsOnlyInRestrictedArea(tb),True)

        #Place one in top right quadrant
        tb[1][7] = 8 
        self.assertEqual(AreHintsOnlyInRestrictedArea(tb),False)
        #put it back
        tb[1][7] = 0
        self.assertEqual(AreHintsOnlyInRestrictedArea(tb),True)

        #Place one in bottom left quadrant
        tb[7][1] = 8 
        self.assertEqual(AreHintsOnlyInRestrictedArea(tb),False)
        #put it back
        tb[7][1] = 0
        self.assertEqual(AreHintsOnlyInRestrictedArea(tb),True)
        
        #Place one in bottom right quadrant
        tb[7][7] = 8 
        self.assertEqual(AreHintsOnlyInRestrictedArea(tb),False)
        #put it back
        tb[7][7] = 0
        self.assertEqual(AreHintsOnlyInRestrictedArea(tb),True)

    def test_hint_board_checker(self):
        tb = CreateExampleTestBoard();
        # 7 0 2 | 0 5 0 | 6 0 0
        # 0 0 0 | 0 0 3 | 0 0 0
        # 1 0 0 | 0 0 9 | 5 0 0
        # ---------------------
        # 8 0 0 | 0 0 0 | 0 9 0
        # 0 4 3 | 0 0 0 | 7 5 0
        # 0 9 0 | 0 0 0 | 0 0 8
        # ---------------------
        # 0 0 9 | 7 0 0 | 0 0 5
        # 0 0 0 | 2 0 0 | 0 0 0
        # 0 0 7 | 0 4 0 | 2 0 3 

        self.assertEqual(checkHintBoard(tb,1),False)#Expect one hint, 24 there
        self.assertEqual(checkHintBoard(tb,24),True)#Expect 24 hints, 24 there

        #Insert 7 on same row
        tb[0][8] = 7
        self.assertEqual(checkHintBoard(tb,25),False)#Expect 25, find 25 but invalid
        #put it back to 0
        tb[0][8] = 0
        self.assertEqual(checkHintBoard(tb,24),True)
        
        #Insert 9 on same column
        tb[8][0] = 1
        self.assertEqual(checkHintBoard(tb,25),False)#Expect 25, find 25 but invalid
        
        #put it back to 0
        tb[8][0] = 0
        self.assertEqual(checkHintBoard(tb,24),True)
        
        #insert 1 on same quadrant (not same row, not same column)
        tb[1][1] = 1
        self.assertEqual(checkHintBoard(tb,25),False)#Expect 25, find 25 but invalid
        
        #put it back to 0
        tb[1][1] = 0
        self.assertEqual(checkHintBoard(tb,24),True)
        
        #Valid insertion
        tb[1][8] = 9
        self.assertEqual(checkHintBoard(tb,25),True)#Expect 25, find 25, all good
        

    def test_hint_board_checker_2(self):
        tb = CreateEmptyBoard();
        
        self.assertEqual(checkHintBoard(tb,0),False)#Expect zero hints, but too many empty groups

        for i in range(0,9):
            tb[0][i] = i + 1
        
        self.assertEqual(checkHintBoard(tb,9),False)#Expect 9 hints, but too many empty groups


    def test_generate_hints(self):
        #Genearte many hint boards with different hints and check
        #40 is number used for easiest sudokus - we go all the way to 45 to be sure
        #Less than 20 may generate invalid boards
       for num_hints in range(20,45):
           board = GetBoardWithHints(num_hints,44);#44 seed works OK
           self.assertEqual(checkHintBoard(board,num_hints), True)
        
    def test_solve_board(self):
        tb = CreateExampleTestBoard();

        self.assertEqual(SolveBoard(tb),True)
        self.assertEqual(checkSolution(tb),True)
        
    def test_get_one_full_puzzle(self):
        num_hints = 41
        result = GetOneFullPuzzle(num_hints, 11814)#11814 seed gives  a fast solution
        self.assertEqual(checkSolution(result["solved_board"]),True)
        self.assertEqual(checkHintBoard(result["board_with_hints"],num_hints), True)
        self.assertEqual(checkSolution(result["board_with_hints"]),False)
        
        
        
        
        
        
        
        