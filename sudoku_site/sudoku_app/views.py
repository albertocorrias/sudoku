import re
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from .models import Game
from .db_generation import GenerateDatabase
import random

from sudoku_app.forms import GameSettingsForm

def index(request):
    
    if (Game.objects.all().count()==0):
        GenerateDatabase(1,1,0,0,11814);#If db is empty, generate one easy and one medium

    game_objects = Game.objects.filter(difficulty = Game.EASY)
    sel_idx = random.randint(0,game_objects.count()-1)
    sel_id = game_objects[sel_idx].id
    request.session['game_type'] = GameSettingsForm.LEISURE #If user lands without any puzzle, start in leisure mode
    return HttpResponseRedirect(reverse('sudoku_app:new_specific_puzzle',  kwargs={'puzzle_id': sel_id}));


def get_context(request, puzzle_id):
    '''
    A helper method that, given a puzzle id, returns a dictionary with
    - A game board object with hints. This is chosen randomly from the database
    - A game board object with he solution.This is chosen randomly from the database
    - A form for further changes to the difficulty level. The form is initialized to the given difficulty level
    - 
    '''
    error_code = 0;
    puzzle_qs = Game.objects.filter(id=puzzle_id);
    if (puzzle_qs.count() == 0):error_code = 1
    if (puzzle_qs.count() >1): error_code = 1

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
            'puzzle_id' : puzzle_id
        }
    else:
        ret = {
            'puzzle_hints': None,
            'puzzle_solution': None,
            'diff_level_form' : None,
            'error_code' : error_code,
            'puzzle_id' : puzzle_id
        }

    return ret

def new_specific_puzzle(request,puzzle_id):
    
    context = get_context(request, puzzle_id)
    if (context["error_code"] == 0):
        template = loader.get_template('sudoku_app/index.html')
    else:
        template = loader.get_template('sudoku_app/error_page.html')
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
