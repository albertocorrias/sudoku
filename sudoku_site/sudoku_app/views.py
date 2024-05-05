import re
import datetime
import json
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.template import loader
from .models import Game,SolvedGame
from .db_generation import GenerateDatabase
from .game_logic import GetOneAlreadySolvedPuzzle,GetOnePuzzliWithOneEmptyColumn
import random

from sudoku_app.forms import GameSettingsForm,SignUpForm

def home(request):
    template = loader.get_template('sudoku_app/home.html')
    user_id=-1
    
    if request.user.is_authenticated:
        user_id = request.user.id
    context = {
        'user_id' : user_id
    }
    return HttpResponse(template.render(context, request))  

def play(request):
    
    if (Game.objects.all().count()==0):
        GenerateDatabase(1,1,0,0,11814);#If db is empty, generate one easy and one medium
    
    #for testing only
    #solved_puzzle = GetOnePuzzliWithOneEmptyColumn()
    #hint_board = solved_puzzle["board_with_hints"]
    #sol_board = solved_puzzle["solved_board"]
    #alreday_solved_game = Game.objects.create(hints_board = hint_board, solved_board = sol_board, difficulty=Game.EXPERT)
    #print(alreday_solved_game.id)

    game_objects = Game.objects.filter(difficulty = Game.EASY)
    sel_idx = random.randint(0,game_objects.count()-1)
    sel_id = game_objects[sel_idx].id
    request.session['game_type'] = GameSettingsForm.LEISURE #If user lands without any puzzle, start in leisure mode
    return HttpResponseRedirect(reverse('sudoku_app:new_specific_puzzle',  kwargs={'puzzle_id': sel_id}));

def sign_up(request):
    if request.method == 'POST':
        sign_up_form = SignUpForm(request.POST)
        if sign_up_form.is_valid():
            sign_up_form.save()
            username = sign_up_form.cleaned_data.get('username')
            raw_password = sign_up_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('sudoku_app:play'))
            else:
                template = loader.get_template('sudoku_app/error_page.html')
                context = {
                'errors': "authentication errors",
                'target_redir_url' : str(647)
                }
                return HttpResponse(template.render(context, request))  

        else:
            game_objects = Game.objects.filter(difficulty = Game.EASY)
            sel_idx = random.randint(0,game_objects.count()-1)
            sel_id = game_objects[sel_idx].id
            template = loader.get_template('sudoku_app/error_page.html')
            context = {
                'errors': sign_up_form.errors,
                'target_redir_url' : str(sel_id)
            }
            return HttpResponse(template.render(context, request))  
    else:
        sign_up_form = SignUpForm()
        

    template = loader.get_template('sudoku_app/sign_up.html')
    context = {
        'sign_up_form' : sign_up_form
    }
    return HttpResponse(template.render(context, request))

def get_context(request, puzzle_id):
    '''
    A helper method that, given a puzzle id, returns a dictionary with
    - A game board object with hints. 
    - A game board object with the solution.
    - A form for further changes to the difficulty level. The form is initialized to the given difficulty level
    - An error code, in case the requested ID is not there or there are multiple ones (the latter should really never happen)
    - The puzzle ID itself for use by the HTML
    '''
    error_code = 0;
    puzzle_qs = Game.objects.filter(id=puzzle_id);
    if (puzzle_qs.count() == 0):error_code = 1
    if (puzzle_qs.count() >1): error_code = 1

    user_id=-1
    if request.user.is_authenticated:
        user_id = request.user.id

    if (error_code ==0):
        puzzle = puzzle_qs.get() #the actual object
        difficulty_level = puzzle.difficulty
        game_type = request.session.get('game_type')
        game_settings_form = GameSettingsForm(initial = {'difficulty_level' : difficulty_level, 'game_type' : game_type})
        ret = {
            'puzzle_hints': puzzle.hints_board,
            'puzzle_solution': puzzle.solved_board,
            'game_settings_form' : game_settings_form,
            'error_code' : error_code,
            'puzzle_id' : puzzle_id,
            'user_id' : user_id
        }
    else:
        ret = {
            'puzzle_hints': None,
            'puzzle_solution': None,
            'diff_level_form' : None,
            'error_code' : error_code,
            'puzzle_id' : puzzle_id,
            'user_id' : user_id
        }

    return ret

def new_specific_puzzle(request,puzzle_id):
    
    context = get_context(request, puzzle_id)
    if (context["error_code"] == 0):
        template = loader.get_template('sudoku_app/play.html')
        return HttpResponse(template.render(context, request))
    else:
        game_objects = Game.objects.filter(difficulty = Game.EASY)
        sel_idx = random.randint(0,game_objects.count()-1)
        sel_id = game_objects[sel_idx].id
        template = loader.get_template('sudoku_app/error_page.html')
        context = {
            'errors': 'An error was encountered. The requested puzzle number ' + str(puzzle_id) + ' does not exist.',
            'target_redir_url' : str(sel_id)
        }
        return HttpResponse(template.render(context, request))  
    

def new_puzzle_from_diff_level_change(request):
    '''
    This method is triggered by the change in level of difficulty form
    '''
    if request.method =='POST':
        form = GameSettingsForm(request.POST)
        if form.is_valid():            
            supplied_diff_level = form.cleaned_data['difficulty_level'];
            supplied_game_type= form.cleaned_data['game_type'];
            game_objects = Game.objects.filter(difficulty = supplied_diff_level)
            sel_idx = random.randint(0,game_objects.count()-1)
            sel_id = game_objects[sel_idx].id
            request.session['game_type'] = supplied_game_type;#Store the game type in the session

    return HttpResponseRedirect(reverse('sudoku_app:new_specific_puzzle',  kwargs={'puzzle_id': sel_id}));

def new_puzzle(request):
    '''
    This method is triggered by the "new game" button
    '''
    if request.method =='POST':
        
        existing_puzzle_id = int(request.POST['new_game_button'])
        existing_puzzle = Game.objects.filter(id=existing_puzzle_id).get();
        difficulty_level = existing_puzzle.difficulty
        game_objects = Game.objects.filter(difficulty = difficulty_level)
        sel_idx = random.randint(0,game_objects.count()-1)
        sel_id = game_objects[sel_idx].id

    return HttpResponseRedirect(reverse('sudoku_app:new_specific_puzzle',  kwargs={'puzzle_id': sel_id})); 

def user_page(request,user_id):
    user = User.objects.filter(id = user_id)
    user_count = user.count()
    if (user_count==1):#one user. We are good
        solved_puzzles = []
        for pzl_solved in SolvedGame.objects.filter(user__id = user_id).order_by(('-time_started')):
            
            solution_details = {
                'puzzle_id' : pzl_solved.game.id,
                'start_time' : pzl_solved.time_started,
                'duration' : pzl_solved.time_solved - pzl_solved.time_started,
                'difficulty' : pzl_solved.game.difficulty
            }
            solved_puzzles.append(solution_details)
        
        template = loader.get_template('sudoku_app/user_page.html')
        context = {
                'name': user.get().username,
                'solved_puzzles' : solved_puzzles
        }
    else:#either no user or, for whatever reason more than one..
        template = loader.get_template('sudoku_app/error_page.html')
        context = {
            'errors': 'An error was encountered. Selected user ID appears not to exist',
        }
    return HttpResponse(template.render(context, request))

def record_successful_puzzle(request):

    user_id=-1
    if request.user.is_authenticated:
        user_id = request.user.id

    if (request.method == 'POST'):

        data = json.loads(request.body)
        
        puzzle_ID = data["puzzle_ID"]
        start_year = data["start_year"]
        start_month = data["start_month"]
        start_day = data["start_day"]
        start_hour = data["start_hour"]
        start_minute = data["start_minute"]
        start_seconds = data["start_seconds"]
        
        end_year = data["end_year"]
        end_month = data["end_month"]
        end_day = data["end_day"]
        end_hour = data["end_hour"]
        end_minute = data["end_minute"]
        end_seconds = data["end_seconds"]
        zone_name = data["zone_name"]

        start_of_puzzle = datetime.datetime(year=start_year, month=start_month, day=start_day, hour=start_hour, minute=start_minute, second = start_seconds)
        end_of_puzzle = datetime.datetime(year=end_year, month=end_month, day=end_day, hour=end_hour, minute=end_minute, second = end_seconds)

        user_query = User.objects.filter(id = user_id)
        if (user_query.count()==1):
            user = user_query.get()
        puzzle_query = Game.objects.filter(id = puzzle_ID)
        if (puzzle_query.count()==1):
            puzzle = puzzle_query.get()
        
        SolvedGame.objects.create(game = puzzle, user = user, time_started = start_of_puzzle, time_solved = end_of_puzzle)

    if (user_id>0):
        return HttpResponseRedirect(reverse('sudoku_app:user_page', kwargs={'user_id' : user_id}));
    else:
        template = loader.get_template('sudoku_app/error_page.html')
        context = {
            'errors': 'An error was encountered. User id not found',
        }
        return HttpResponse(template.render(context, request))

