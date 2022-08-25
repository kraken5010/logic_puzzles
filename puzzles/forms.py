from django import forms
from django.core.exceptions import ValidationError

from .models import *

curse_words = ['Cunt', 'motherfucker', 'fuck', 'bitch', 'ass', 'cock', 'dick', 'dickhead', 'pussy', 'beaver', 'shit', 'son of a bitch', 'bollocks', 'bullshit', 'feck', 'arsehole']


class AddUserPuzzleForm(forms.ModelForm):
    """Form for adding an entry to the UserPuzzle table"""
    class Meta:
        model = UserPuzzle
        fields = ['title', 'question', 'answer']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Puzzles title'}),
            'question': forms.Textarea(attrs={'placeholder': 'Puzzles question'}),
            'answer': forms.Textarea(attrs={'placeholder': 'Puzzles title'}),
        }

    # Title field validation
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Length exceeds 50 characters!')

        for item in str(title).lower().split():
            if item in curse_words:
                raise ValidationError('Swear words are prohibited !!!')
        return title