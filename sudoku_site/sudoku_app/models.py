from django.contrib.postgres.fields import ArrayField
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
    
class CurrentDifficultyLevel(models.Model):
    current_level = models.CharField(max_length = 50, choices = Game.DIFFICULTY_LEVELS, default=Game.EASY)