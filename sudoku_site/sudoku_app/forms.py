from enum import unique
from django import forms
from .models import Game
from django.forms import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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


class SignUpForm(UserCreationForm):

    email = forms.EmailField(required=True, help_text="Requuired. Enter a valid email address")

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with the same email already exists")
        return self.cleaned_data

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
