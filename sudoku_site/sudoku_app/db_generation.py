from sudoku_app.game_logic import GetOneFullPuzzle
from .models import Game

def GenerateDatabase():
    #clear any existing
    print("Hello, generating database")
    Game.objects.all().delete()
    print("All clear")


    num_puzzles = 4
    num_hints  = 40
    for i in range(0,num_puzzles):
        puzzle = GetOneFullPuzzle(num_hints)
        print(i)
        hint_board = puzzle["board_with_hints"]
        sol_board = puzzle["solved_board"]

        Game.objects.create(hints_board = hint_board, solved_board = sol_board, difficulty=Game.EASY)
    print("Done with easy ones")
    
    
    num_hints  = 30
    for i in range(0,num_puzzles):
        puzzle = GetOneFullPuzzle(num_hints)
        print(i)
        hint_board = puzzle["board_with_hints"]
        sol_board = puzzle["solved_board"]

        Game.objects.create(hints_board = hint_board, solved_board = sol_board, difficulty=Game.MEDIUM)
    print("Done with medium ones")

    num_hints  = 25
    for i in range(0,num_puzzles):
        puzzle = GetOneFullPuzzle(num_hints)
        print(i)
        hint_board = puzzle["board_with_hints"]
        sol_board = puzzle["solved_board"]

        Game.objects.create(hints_board = hint_board, solved_board = sol_board, difficulty=Game.HARD)
    print("Done with hard ones")

    num_hints  = 23
    for i in range(0,num_puzzles):
        puzzle = GetOneFullPuzzle(num_hints)
        print(i)
        hint_board = puzzle["board_with_hints"]
        sol_board = puzzle["solved_board"]

        Game.objects.create(hints_board = hint_board, solved_board = sol_board, difficulty=Game.EXPERT)
    print("Done with expert ones")

