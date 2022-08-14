from django import forms
from .models import Game

class GameSettingsForm(forms.Form):
    LEISURE = 'Leisure'
    TIMED = 'Timed'
    GAME_TYPES = [
        (LEISURE, 'Leisure'),
        (TIMED, 'Timed'),
    ]
    difficulty_level = forms.ChoiceField(choices=Game.DIFFICULTY_LEVELS, label='Difficulty',\
                                     widget=forms.Select(attrs={'onchange': 'submit();'}))
    
    game_type = forms.ChoiceField(choices=GAME_TYPES, label='Type',\
                                     widget=forms.Select(attrs={'onchange': 'submit();'}))