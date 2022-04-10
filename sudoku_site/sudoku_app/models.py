from django.contrib.postgres.fields import ArrayField
from django.db import models

class SuokuGame(models.Model):
    game_board = ArrayField(models.IntegerField(), size=81)
    
