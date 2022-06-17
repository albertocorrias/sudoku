from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from .models import Game, CurrentDifficultyLevel
from .db_generation import GenerateDatabase
import random

from sudoku_app.forms import DifficultyLevelForm
def index(request):
    template = loader.get_template('sudoku_app/index.html')
    if (Game.objects.all().count()==0):
        GenerateDatabase();
    #Check if any current difficulty level was set
    diff_level = Game.EASY
    if (CurrentDifficultyLevel.objects.all().count() == 0):
        CurrentDifficultyLevel.objects.create(current_level=Game.EASY)
    else:
        diff_level = CurrentDifficultyLevel.objects.values_list("current_level", flat=True)[0]
    

    game_objects = Game.objects.filter(difficulty = diff_level)
    sel_idx = random.randint(0,game_objects.count()-1)
    puzzle = game_objects[sel_idx]
    
    diff_level_form = DifficultyLevelForm(initial = {'difficulty_level' : diff_level})
    context = {
        'puzzle_hints': puzzle.hints_board,
        'puzzle_solution': puzzle.solved_board,
        'diff_level_form' : diff_level_form
    }
    return HttpResponse(template.render(context, request))

def new_puzzle(request):
    if request.method =='POST':
        form = DifficultyLevelForm(request.POST)
    
        if form.is_valid():            
            supplied_diff_level = form.cleaned_data['difficulty_level'];
            first_id = CurrentDifficultyLevel.objects.first().id
            CurrentDifficultyLevel.objects.filter(id = first_id).update(current_level = supplied_diff_level)

    return HttpResponseRedirect(reverse('sudoku_app:index'));
