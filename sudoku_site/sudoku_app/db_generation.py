from sudoku_app.game_logic import GetOneFullPuzzle
from .models import Game

def GenerateDatabase(num_easy, num_medium, num_hard, num_expert,deterministic_seed=None):
    #clear any existing
    print("Clearing any puzzle in existing database")
    Game.objects.all().delete()
    print("All clear, generating puzzles now...")

    num_hints  = 40
    for i in range(0,num_easy):
        puzzle = GetOneFullPuzzle(num_hints, deterministic_seed)
        print(i)
        hint_board = puzzle["board_with_hints"]
        sol_board = puzzle["solved_board"]

        Game.objects.create(hints_board = hint_board, solved_board = sol_board, difficulty=Game.EASY)
    print("Done with easy ones")
    
    
    num_hints  = 30
    for i in range(0,num_medium):
        puzzle = GetOneFullPuzzle(num_hints,deterministic_seed)
        print(i)
        hint_board = puzzle["board_with_hints"]
        sol_board = puzzle["solved_board"]

        Game.objects.create(hints_board = hint_board, solved_board = sol_board, difficulty=Game.MEDIUM)
    print("Done with medium ones")

    num_hints  = 25
    for i in range(0,num_hard):
        puzzle = GetOneFullPuzzle(num_hints,deterministic_seed)
        print(i)
        hint_board = puzzle["board_with_hints"]
        sol_board = puzzle["solved_board"]

        Game.objects.create(hints_board = hint_board, solved_board = sol_board, difficulty=Game.HARD)
    print("Done with hard ones")

    num_hints  = 23
    for i in range(0,num_expert):
        puzzle = GetOneFullPuzzle(num_hints, deterministic_seed)
        print(i)
        hint_board = puzzle["board_with_hints"]
        sol_board = puzzle["solved_board"]

        Game.objects.create(hints_board = hint_board, solved_board = sol_board, difficulty=Game.EXPERT)
    print("Done with expert ones")

