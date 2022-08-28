from django import forms
from .models import Game

class GameSettingsForm(forms.Form):
    LEISURE = 'Leisure'
    TIMED = 'Timed' #NOTE This is picked up by JS. If changed, JS need toc hange as well
    GAME_TYPES = [
        (LEISURE, 'Leisure'),
        (TIMED, 'Timed'),
    ]
    ID_OF_GAME_TYPE_ELEMENT = 'id_game_type' #NOTE this is picked up by JS. If you cahnge this, change JS as well.

    difficulty_level = forms.ChoiceField(choices=Game.DIFFICULTY_LEVELS, label='Difficulty',\
                                     widget=forms.Select(attrs={'onchange': 'submit();'}))
    
    game_type = forms.ChoiceField(choices=GAME_TYPES, label='Type',\
                                     widget=forms.Select(attrs={'onchange': 'submit();', 'id': ID_OF_GAME_TYPE_ELEMENT}))