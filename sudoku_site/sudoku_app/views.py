from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from sudoku_app.game_logic import GetOneFullPuzzle

def index(request):
    template = loader.get_template('sudoku_app/index.html')

    puzzle = GetOneFullPuzzle(30,42)
    
    context = {
        'puzzle_hints': puzzle["board_with_hints"],
        'puzzle_solution': puzzle["solved_board"]
    }
    return HttpResponse(template.render(context, request))
