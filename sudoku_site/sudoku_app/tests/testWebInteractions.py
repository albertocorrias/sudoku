import copy
from django.test import LiveServerTestCase
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from decimal import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from sudoku_app.models import Game
from sudoku_app.game_logic import CreateEmptyBoard, SolveBoard


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

class TestWebInteractions(LiveServerTestCase):

    def test_driver_manager_chrome(self):
        service = ChromeService(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        #set up a puzzle
        hint_brd = CreateExampleTestBoard()
        saved_hints = copy.deepcopy(hint_brd)
        slv = SolveBoard(hint_brd)#hint_brd becomes solved. Note slv is just a flag
        Game.objects.create(hints_board = saved_hints, solved_board = hint_brd, difficulty=Game.EASY)

        driver.get('http://127.0.0.1:8000/')
        
        self.assertEqual(Game.objects.all().count(), 1)
        
        driver.quit()
        