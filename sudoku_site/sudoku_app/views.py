from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from .models import Game
from .db_generation import GenerateDatabase
import random

from sudoku_app.forms import DifficultyLevelForm

def index(request):
    
    if (Game.objects.all().count()==0):
        GenerateDatabase();

    game_objects = Game.objects.filter(difficulty = Game.EASY)
    sel_idx = random.randint(0,game_objects.count()-1)
    sel_id = game_objects[sel_idx].id
    return HttpResponseRedirect(reverse('sudoku_app:new_spec_puzzle',  kwargs={'puzzle_id': sel_id}));


def set_up_new_puzzle(puzzle_id):
    '''
    A helper method that, given a puzzle id, returns a dictionary with
    - A game board object with hints. This is chosen randomly from the database
    - A game board object with he solution.This is chosen randomly from the database
    - A form for further changes to the difficulty level. the form is initialized to the given difficulty level
    '''
    puzzle = Game.objects.filter(id=puzzle_id).get()
    difficulty_level = puzzle.difficulty
    diff_level_form = DifficultyLevelForm(initial = {'difficulty_level' : difficulty_level})
    ret = {
        'puzzle_hints': puzzle.hints_board,
        'puzzle_solution': puzzle.solved_board,
        'diff_level_form' : diff_level_form
    }
    return ret

def new_specific_puzzle(request,puzzle_id):
    
    context = set_up_new_puzzle(puzzle_id)
    template = loader.get_template('sudoku_app/index.html')
    return HttpResponse(template.render(context, request))

def new_puzzle(request):
    if request.method =='POST':
        form = DifficultyLevelForm(request.POST)
    
        if form.is_valid():            
            supplied_diff_level = form.cleaned_data['difficulty_level'];
            game_objects = Game.objects.filter(difficulty = supplied_diff_level)
            sel_idx = random.randint(0,game_objects.count()-1)
            sel_id = game_objects[sel_idx].id

    return HttpResponseRedirect(reverse('sudoku_app:new_spec_puzzle',  kwargs={'puzzle_id': sel_id}));
