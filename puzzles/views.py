from rest_framework import generics
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import *
from .serializers import PuzzleSerializer

menu = [
    {'title': 'Main puzzles', 'url_name': 'main_puzzles'},
    {'title': 'Users puzzles', 'url_name': 'users_puzzles'},
    {'title': 'Propose a puzzle', 'url_name': 'propose_puzzle'},
    {'title': 'About app', 'url_name': 'about_app'}
]


# Main page
def main_puzzles(request):
    puzzles = Puzzle.objects.all()
    context = {
        'menu': menu,
        'title': 'Logic puzzles',
        'puzzles': puzzles
    }
    return render(request, 'main_puzzles.html', context=context)


def puzzle_detail(request, puzzle_slug):
    puzzle = Puzzle.objects.get(slug=puzzle_slug)
    try:
        next_puzzle = Puzzle.objects.get(pk=int(puzzle.id + 1))
    except:
        next_puzzle = None

    try:
        prev_puzzle = Puzzle.objects.get(pk=int(puzzle.id - 1))
    except:
        prev_puzzle = None

    context = {
        'menu': menu,
        'puzzle': puzzle,
        'title': puzzle.title,
        'next_puzzle': next_puzzle,
        'prev_puzzle': prev_puzzle
    }
    return render(request, 'puzzle_detail.html', context=context)


def users_puzzles(request):
    users_puzzles = UserPuzzle.objects.filter(draft=True)
    context = {
        'menu': menu,
        'title': 'Users puzzles',
        'users_puzzles': users_puzzles
    }
    return render(request, 'users_puzzles.html', context=context)


def user_puzzle_detail(request, user_puzzle_slug):
    puzzle = UserPuzzle.objects.get(slug=user_puzzle_slug)
    try:
        next_puzzle = UserPuzzle.objects.get(pk=int(puzzle.id + 1))
    except:
        next_puzzle = None

    try:
        prev_puzzle = UserPuzzle.objects.get(pk=int(puzzle.id - 1))
    except:
        prev_puzzle = None

    context = {
        'menu': menu,
        'puzzle': puzzle,
        'title': puzzle.title,
        'next_puzzle': next_puzzle,
        'prev_puzzle': prev_puzzle
    }
    return render(request, 'user_puzzle_detail.html', context=context)


def propose_puzzle(request):
    current_user = request.user
    if request.method == 'POST':
        form = AddUserPuzzleForm(request.POST)
        if form.is_valid():
            puzzle = form.save(commit=False)
            puzzle.username = current_user.username
            puzzle.email = current_user.email
            print(puzzle.email)
            puzzle.save()
        return redirect('users_puzzles')
    else:
        form = AddUserPuzzleForm()

    context = {
        'menu': menu,
        'title': 'Propose a puzzle',
        'form': form
    }
    return render(request, 'propose_puzzle.html', context=context)


def about_app(request):
    context = {
        'menu': menu,
        'title': 'About app',
    }
    return render(request, 'about_app.html', context=context)


def sign_up(request):
    """Authorization"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Auto login user after register
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()

    context = {
        'menu': menu,
        'title': 'Sign up',
        'form': form
    }
    return render(request, 'sign_up.html', context=context)


class SignInUser(LoginView):
    """Authentication"""
    form_class = SignInForm
    template_name = 'sign_in.html'

    def get_context_data(self, **kwargs):
        context = {
            'menu': menu,
            'title': 'Sign in',
            'form': self.form_class
        }
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('sign_in')


class PuzzleAPIView(generics.ListAPIView):
    queryset = Puzzle.objects.all()
    serializer_class = PuzzleSerializer
