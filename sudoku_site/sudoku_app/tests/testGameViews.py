import copy
from datetime import datetime, timedelta, timezone
from django.test import TestCase
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from decimal import *
from sudoku_app.models import Game,SolvedGame
from sudoku_app.game_logic import CreateEmptyBoard, SolveBoard
from sudoku_app.forms import GameSettingsForm,SignUpForm

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

class TestGameViews(TestCase):
    
    def test_index_empty_db(self):
        response = self.client.get(reverse('sudoku_app:index'))
        self.assertEqual(response.status_code, 302) #Should re-direct...

    def test_index_non_empty_db(self):
        hint_brd = CreateExampleTestBoard()
        saved_hints = copy.deepcopy(hint_brd)
        solved = SolveBoard(hint_brd)
        Game.objects.create(hints_board = saved_hints, solved_board = hint_brd, difficulty=Game.EASY)
        
        self.assertEqual(Game.objects.all().count(), 1)
        self.assertEqual(Game.objects.filter(difficulty=Game.EASY).count(), 1)

        response = self.client.get(reverse('sudoku_app:index'))
        self.assertEqual(response.status_code, 302) #Should re-direct...
        expected_url = '/' + str(Game.objects.filter(difficulty=Game.EASY).get().id)#Only one there anyway...
        self.assertRedirects(response, expected_url, status_code=302,target_status_code=200)

    def test_new_specific_puzzle(self):
        hint_brd = CreateExampleTestBoard()
        saved_hints = copy.deepcopy(hint_brd)
        solved = SolveBoard(hint_brd)
        Game.objects.create(hints_board = saved_hints, solved_board = hint_brd, difficulty=Game.EASY)
        self.assertEqual(Game.objects.all().count(), 1)

        session = self.client.session
        session['game_type'] = GameSettingsForm.LEISURE
        session.save()

        id_of_puzzle = Game.objects.filter(difficulty=Game.EASY).get().id
        response = self.client.get(reverse('sudoku_app:new_specific_puzzle', kwargs={'puzzle_id': id_of_puzzle}))
        self.assertEqual(response.status_code, 200)#no issues

        #Now try an Id that does not exist
        response = self.client.get(reverse('sudoku_app:new_specific_puzzle', kwargs={'puzzle_id': id_of_puzzle+25987}))
        self.assertEqual(response.status_code, 200)#still no issues, error page should appear instead
        self.assertContains(response, 'error')

    def test_new_puzzle_button(self):
        hint_brd = CreateExampleTestBoard()
        saved_hints = copy.deepcopy(hint_brd)
        solved = SolveBoard(hint_brd)
        #Here, we create two (even if identical)
        Game.objects.create(hints_board = saved_hints, solved_board = hint_brd, difficulty=Game.EASY)
        Game.objects.create(hints_board = saved_hints, solved_board = hint_brd, difficulty=Game.EASY)
        self.assertEqual(Game.objects.all().count(), 2)

        session = self.client.session
        session['game_type'] = GameSettingsForm.LEISURE
        session.save()

        one_id = Game.objects.all().first().id
        other_id = Game.objects.all().last().id
        response = self.client.get(reverse('sudoku_app:new_specific_puzzle', kwargs={'puzzle_id': one_id}))
        self.assertEqual(response.status_code, 200)#no issues

        session = self.client.session
        session['game_type'] = GameSettingsForm.LEISURE
        session.save()

        response = self.client.post(reverse('sudoku_app:new_puzzle'), {'new_game_button': one_id})
        self.assertEqual(response.status_code, 302)#should re-direct

        #There are two possible urls as there are two possible puzzles
        possible_urls = ['/'+str(one_id), '/'+str(other_id)]
        all_good = False
        if response.url in possible_urls:
            all_good = True
        self.assertEquals(all_good, True)

    def test_difficulty_level_change(self):
        hint_brd = CreateExampleTestBoard()
        saved_hints = copy.deepcopy(hint_brd)
        solved = SolveBoard(hint_brd)
        #Here, we create two (even if identical, but with different levels of difficulty)
        Game.objects.create(hints_board = saved_hints, solved_board = hint_brd, difficulty=Game.EASY)
        Game.objects.create(hints_board = saved_hints, solved_board = hint_brd, difficulty=Game.MEDIUM)
        self.assertEqual(Game.objects.all().count(), 2)

        session = self.client.session
        session['game_type'] = GameSettingsForm.LEISURE
        session.save()

        easy_ID = Game.objects.filter(difficulty=Game.EASY).get().id
        medium_id = Game.objects.filter(difficulty=Game.MEDIUM).get().id
        response = self.client.get(reverse('sudoku_app:new_specific_puzzle', kwargs={'puzzle_id': easy_ID}))
        self.assertEqual(response.status_code, 200)#no issues


        response = self.client.post(reverse('sudoku_app:new_puzzle_from_diff_level_change'), \
                                    {'difficulty_level': Game.MEDIUM, 'game_type' : GameSettingsForm.LEISURE})
        self.assertEqual(response.status_code, 302)#should re-direct
        expected_url = '/' + str(medium_id)
        self.assertRedirects(response, expected_url, status_code=302,target_status_code=200)

    def test_sign_up_form(self): 
        empty_sign_up_form = SignUpForm();
        self.assertEqual(empty_sign_up_form.is_valid(), False)
        
        user_name = 'test_user'
        password = 'Hello12349865'
        email = 'myemail@me.com'
        filled_form = SignUpForm(data={'username': user_name,'email' : email, 'password1' : password, 'password2' : password})
        self.assertEqual(filled_form.is_valid(), True)

    def test_sign_up(self):
        hint_brd = CreateExampleTestBoard()
        saved_hints = copy.deepcopy(hint_brd)
        solved = SolveBoard(hint_brd)
        #Here, we create two (even if identical, but with different levels of difficulty)
        Game.objects.create(hints_board = saved_hints, solved_board = hint_brd, difficulty=Game.EASY)
        Game.objects.create(hints_board = saved_hints, solved_board = hint_brd, difficulty=Game.MEDIUM)
        self.assertEqual(Game.objects.all().count(), 2)
        easy_ID = Game.objects.filter(difficulty=Game.EASY).get().id
    
        #go to sign-up page, to test the GET
        response = self.client.get(reverse('sudoku_app:sign_up'))
        self.assertEqual(response.status_code, 200)#no issues
        #No user at the start
        self.assertEqual(User.objects.all().count(),0)
        #Nobody authenticated
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, False)

        #add a user
        user_name = 'test_user'
        password = 'Hello12349865'
        email = 'myemail@me.com'
        self.client.post(reverse('sudoku_app:sign_up'),{'username': user_name,'email' : email, 'password1' : password, 'password2' : password})
        self.assertEqual(User.objects.all().count(),1)
        self.assertEqual(User.objects.filter(username=user_name).count(),1)
        response = self.client.get(reverse('sudoku_app:new_specific_puzzle', kwargs={'puzzle_id': easy_ID}))
        self.assertEqual(response.status_code, 200)#no issues
        
        #The view is coded up to autmatically authenticate the user, so we test that it is actually so (unlike before)
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)

        #Try adding a user wth the same user name, but different email
        email_new = 'youremail@you.com'
        self.client.post(reverse('sudoku_app:sign_up'),{'username': user_name,'email' : email_new, 'password1' : password, 'password2' : password})
        #Should still be 1
        self.assertEqual(User.objects.all().count(),1)
        self.assertEqual(User.objects.filter(username=user_name).count(),1)
        
        #Try adding a user wth the same email, but different username
        uesr_new = 'another_user'
        self.client.post(reverse('sudoku_app:sign_up'),{'username': uesr_new,'email' : email, 'password1' : password, 'password2' : password})
        #Should still be 1
        self.assertEqual(User.objects.all().count(),1)
        self.assertEqual(User.objects.filter(username=user_name).count(),1)

    def test_store_good_result(self):
        hint_brd = CreateExampleTestBoard()
        saved_hints = copy.deepcopy(hint_brd)
        solved = SolveBoard(hint_brd)
        #Here, we create two (even if identical, but with different levels of difficulty)
        Game.objects.create(hints_board = saved_hints, solved_board = hint_brd, difficulty=Game.EASY)
        Game.objects.create(hints_board = saved_hints, solved_board = hint_brd, difficulty=Game.MEDIUM)
        self.assertEqual(Game.objects.all().count(), 2)
        easy_ID = Game.objects.filter(difficulty=Game.EASY).get().id
        #add a user
        user_name = 'test_user'
        password = 'Hello12349865'
        email = 'myemail@me.com'
        self.client.post(reverse('sudoku_app:sign_up'),{'username': user_name,'email' : email, 'password1' : password, 'password2' : password})
        self.assertEqual(User.objects.all().count(),1)
        self.assertEqual(User.objects.filter(username=user_name).count(),1)
        response = self.client.get(reverse('sudoku_app:new_specific_puzzle', kwargs={'puzzle_id': easy_ID}))
        self.assertEqual(response.status_code, 200)#no issues
        
        #The view is coded up to autmatically authenticate the user, so we test that it is actually so (unlike before)
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        #No solved game to start with
        self.assertEqual(SolvedGame.objects.all().count(),0)
        puzzle_start = datetime.now(timezone.utc)
        puzzle_end  = puzzle_start + timedelta(hours=1, minutes=2, seconds=4)

        #Test the post to store a successful game for the user
        response = self.client.post(reverse('sudoku_app:record_successful_puzzle'), {'puzzle_ID' : easy_ID, 'time_started' : puzzle_start, 'time_finished'  :puzzle_end})

        #Now should be 1
        self.assertEqual(SolvedGame.objects.all().count(),1)
        
        #Check re-direction
        expected_url = '/user/' + str(User.objects.filter(username=user_name).get().id) + '/'
        self.assertRedirects(response, expected_url, status_code=302,target_status_code=200)