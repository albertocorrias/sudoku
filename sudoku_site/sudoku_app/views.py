from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from .models import Game
from sudoku_app.game_logic import GetOneFullPuzzle
from sudoku_app.db_generation import GenerateDatabase
from sudoku_app.forms import DifficultyLevelForm
def index(request):
    template = loader.get_template('sudoku_app/index.html')

    print(Game.objects.all().count())
    first_id = Game.objects.first().id
    puzzle = Game.objects.get(id=first_id+15)
    
    diff_level = DifficultyLevelForm()
    context = {
        'puzzle_hints': puzzle.hints_board,
        'puzzle_solution': puzzle.solved_board,
        'diff_level_form' : diff_level
    }
    return HttpResponse(template.render(context, request))

def new_puzzle():
    print('hello')