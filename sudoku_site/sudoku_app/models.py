from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.db import models

class Game(models.Model):
    EASY = 'Easy'
    MEDIUM = 'Medium'
    HARD = 'Hard'
    EXPERT = 'Expert'
    
    DIFFICULTY_LEVELS = [
        (EASY, 'Easy'),
        (MEDIUM, 'Medium'),
        (HARD, 'Hard'),
        (EXPERT, 'Expert'),
    ]

    hints_board = ArrayField( ArrayField(models.IntegerField(), size=9), size=9)
    solved_board = ArrayField( ArrayField(models.IntegerField(), size=9), size=9)
    difficulty = models.CharField(max_length = 50, choices = DIFFICULTY_LEVELS, default=EASY)
    

class SolvedGame(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE) #The game being solved
    user = models.ForeignKey(User, on_delete=models.CASCADE) #the user who solved it
    time_started = models.DateTimeField() #Time when the solution started
    time_solved = models.DateTimeField() #Time when correct solution was submitted