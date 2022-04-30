from django import forms
from .models import Game

class DifficultyLevelForm(forms.Form):

    difficulty_level = forms.ChoiceField(choices=Game.DIFFICULTY_LEVELS, label='')#), default=Game.EASY)