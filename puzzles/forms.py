from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import *

curse_words = ['Cunt', 'motherfucker', 'fuck', 'bitch', 'ass', 'cock', 'dick', 'dickhead', 'pussy', 'beaver', 'shit', 'son of a bitch', 'bollocks', 'bullshit', 'feck', 'arsehole']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        # fields = '__all__'
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Your login'}),
            'email': forms.TextInput(attrs={'placeholder': 'Your email'}),
            'password1': forms.TextInput(attrs={'placeholder': 'Your password', 'type': 'password'}),
            'password2': forms.TextInput(attrs={'placeholder': 'Repeat password', 'type': 'password'})
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        # fields = '__all__'
        fields = ('username', 'email', 'phone', 'gender', 'birth_date', 'photo')


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


class SignInForm(AuthenticationForm):
    username = forms.CharField(max_length=50, label='Login', widget=forms.TextInput(attrs={'placeholder': 'Your login'}))
    password = forms.CharField(max_length=50, label='Password', widget=forms.TextInput(attrs={'placeholder': 'Your password', 'type': 'password'}))


class CommentForm(forms.ModelForm):
    """Comment Form"""
    class Meta:
        model = Comment
        exclude = ['user']
        fields = ['text', 'parent']
        widgets = {
            'text': forms.Textarea(attrs={'id': 'contactcomment', 'rows': 2, 'placeholder': 'Your comment'}),
            'parent': forms.TextInput(attrs={'type': 'hidden', 'id': 'contactparent'})
        }


