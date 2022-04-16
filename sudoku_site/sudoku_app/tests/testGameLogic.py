from django.test import TestCase
from django.urls import reverse
from decimal import *
from sudoku_app.game_logic import GetOneFullPuzzle,GetBoardWithHints,\
isValidAllocation,howManyTimesInQuadrant,howManyTimesInRow,howManyTimesInColumn,\
CreateEmptyBoard, SolveBoard,checkSolution, checkHintBoard


class TestGameLogic(TestCase):
    
    def test_create_empty_board(self):
        tb = CreateEmptyBoard();
        self.assertEqual(len(tb),9)
        for i in range(0,len(tb)):
            self.assertEqual(len(tb[i]),9)
            for k in range(0,len(tb[i])):
                self.assertEqual(tb[i][k],0)
                
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
    
    def test_hint_board_checker(self):
        tb = CreateEmptyBoard();
        
        self.assertEqual(checkHintBoard(tb,1),False)#Expect one hint, none there
        tb[0][0] = 9
        self.assertEqual(checkHintBoard(tb,1),True)#Expect one hint, one there
        #Insert 9 on same row
        tb[0][8] = 9
        self.assertEqual(checkHintBoard(tb,2),False)#Expect two, find two but invalid
        #put it back to 0
        tb[0][8] = 0
        self.assertEqual(checkHintBoard(tb,1),True)
        
        #Insert 9 on same column
        tb[8][0] = 9
        self.assertEqual(checkHintBoard(tb,2),False)#Expect two, find two but invalid
        
        #put it back to 0
        tb[8][0] = 0
        self.assertEqual(checkHintBoard(tb,1),True)
        
        #insert 9 on same quadrant
        tb[1][1] = 9
        self.assertEqual(checkHintBoard(tb,2),False)#Expect two, find two but invalid
        
        #put it back to 0
        tb[1][1] = 0
        self.assertEqual(checkHintBoard(tb,1),True)
        
        #Valid 9 insertion
        tb[1][8] = 9
        self.assertEqual(checkHintBoard(tb,2),True)#Expect two, find two
        
        #Valid non-9 insertion in same quadrant
        tb[1][1] = 4
        self.assertEqual(checkHintBoard(tb,3),True)#Expect three, find three
        
        #Valid non-9 insertion in same row
        tb[0][8] = 1
        self.assertEqual(checkHintBoard(tb,4),True)#Expect 4, find 4
        
        #Valid non-9 insertion in same column
        tb[8][0] = 2
        self.assertEqual(checkHintBoard(tb,5),True)#Expect 5, find 5
        
    def test_generate_hints(self):
        #Genearte many hint boards with different hints and check
        #40 is number used for easiest sudokus - we go all the way to 45 to be sure
        for num_hints in range(1,45):
            board = GetBoardWithHints(num_hints,45);#45 seed works OK
            self.assertEqual(checkHintBoard(board,num_hints), True)
        
    def test_solve_board(self):
        tb = CreateEmptyBoard();
        #set it up like in the solver's video
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

        self.assertEqual(SolveBoard(tb),True)
        self.assertEqual(checkSolution(tb),True)
        
    def test_get_one_full_puzzle(self):
        num_hints = 29
        result = GetOneFullPuzzle(num_hints, 44)#44 seed gives  a fast solution
        self.assertEqual(checkSolution(result["solved_board"]),True)
        self.assertEqual(checkHintBoard(result["board_with_hints"],num_hints), True)
        self.assertEqual(checkSolution(result["board_with_hints"]),False)
        
        
        
        
        
        
        
        