from django.test import TestCase
from django.urls import reverse
from decimal import *
from sudoku_app.game_logic import GetOneFullPuzzle,GetBoardWithHints,\
isValidAllocation,isPresentInQuadrant,isPresentInRow,isPresentInColumn,\
CreateEmptyBoard, SolveBoard,checkSolution


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
                        self.assertEqual(isPresentInRow(num_to_try,row,tb),True)
                    else:
                        self.assertEqual(isPresentInRow(num_to_try,row,tb),False)
                else:
                    self.assertEqual(isPresentInRow(num_to_try,row,tb),False)
                    
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
                        self.assertEqual(isPresentInColumn(num_to_try,col,tb),True)
                    else:
                        self.assertEqual(isPresentInColumn(num_to_try,col,tb),False)
                else:
                    self.assertEqual(isPresentInColumn(num_to_try,col,tb),False)
                        
                
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
                            self.assertEqual(isPresentInQuadrant(num_to_try,row,col,tb),True)
                        else:
                            self.assertEqual(isPresentInQuadrant(num_to_try,row,col,tb),False)
                    else:
                        self.assertEqual(isPresentInQuadrant(num_to_try,row,col,tb),False)
                    
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
                            self.assertEqual(isPresentInQuadrant(num_to_try,row,col,tb),True)
                        else:
                            self.assertEqual(isPresentInQuadrant(num_to_try,row,col,tb),False)
                    else:
                        self.assertEqual(isPresentInQuadrant(num_to_try,row,col,tb),False)         
    
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
        
        
        
        
        
        
        
        
        
        