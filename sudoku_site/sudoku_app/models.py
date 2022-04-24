from django.contrib.postgres.fields import ArrayField
from django.db import models

class SuokuGame(models.Model):
    game_board = ArrayField(models.IntegerField(), size=81)

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
    
