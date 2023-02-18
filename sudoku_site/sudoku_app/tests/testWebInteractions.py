import copy
import time
from django.test import LiveServerTestCase
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from decimal import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from sudoku_app.models import Game, SolvedGame
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
        self.assertEqual(SolvedGame.objects.all().count(),0)

        user_name = 'test_user'
        password = 'Hello12349865'
        email = 'myemail@me.com'
        self.client.post(reverse('sudoku_app:sign_up'),{'username': user_name,'email' : email, 'password1' : password, 'password2' : password})
        self.assertEqual(User.objects.all().count(),1)

        service = ChromeService(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        #set up a puzzle
        hint_brd = CreateExampleTestBoard()
        #saved_hints = copy.deepcopy(hint_brd)
        slv = SolveBoard(hint_brd)#hint_brd becomes solved. Note slv is just a flag

        #Here, we create a puzzle that is fully solved, by passing the solved board (hint_brd after the solve routine) as the hint board
        new_game = Game.objects.create(hints_board = hint_brd, solved_board = hint_brd, difficulty=Game.EASY)
        self.assertEqual(Game.objects.all().count(), 1)
        driver.get('http://127.0.0.1:8000/')#+str(new_game.id))
        driver.find_element(By.ID, "check_answers_button").click()

        time.sleep(10)
        driver.quit()
        self.assertEqual(SolvedGame.objects.all().count(),1)
        