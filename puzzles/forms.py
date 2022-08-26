from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
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


class SignUpForm(UserCreationForm):
    """Register user form"""
    username = forms.CharField(max_length=50, label='Login', widget=forms.TextInput(attrs={'placeholder': 'Your login'}))
    email = forms.CharField(max_length=50, label='Email', widget=forms.TextInput(attrs={'placeholder': 'Your email'}))
    password1 = forms.CharField(max_length=255, label='Password', widget=forms.TextInput(attrs={'placeholder': 'Your password', 'type': 'password'}))
    password2 = forms.CharField(max_length=255, label='Repeat password', widget=forms.TextInput(attrs={'placeholder': 'Repeat password', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    # Change password validation
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match')
        return password2


class SignInForm(AuthenticationForm):
    username = forms.CharField(max_length=50, label='Login', widget=forms.TextInput(attrs={'placeholder': 'Your login'}))
    password = forms.CharField(max_length=50, label='Password', widget=forms.TextInput(attrs={'placeholder': 'Your password', 'type': 'password'}))

    class Meta:
        model = User
        fields = '__all__'


