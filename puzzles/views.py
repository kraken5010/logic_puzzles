from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import *
from .forms import *

menu_login = [
    {'title': 'sign in', 'url_name': 'sign_in'},
    {'title': 'sign up', 'url_name': 'sign_up'}
]
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
        'menu_login': menu_login,
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
        'menu_login': menu_login,
        'menu': menu,
        'puzzle': puzzle,
        'title': puzzle.title,
        'next_puzzle': next_puzzle,
        'prev_puzzle': prev_puzzle
    }
    return render(request, 'puzzle_detail.html', context=context)


def sign_in(request):
    return HttpResponse('About app')


def sign_up(request):
    return HttpResponse('About app')


def users_puzzles(request):
    users_puzzles = UserPuzzle.objects.all()
    context = {
        'menu_login': menu_login,
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
        'menu_login': menu_login,
        'menu': menu,
        'puzzle': puzzle,
        'title': puzzle.title,
        'next_puzzle': next_puzzle,
        'prev_puzzle': prev_puzzle
    }
    return render(request, 'user_puzzle_detail.html', context=context)


def propose_puzzle(request):
    if request.method == 'POST':
        form = AddUserPuzzleForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = AddUserPuzzleForm()

    context = {
        'menu_login': menu_login,
        'menu': menu,
        'title': 'Propose a puzzle',
        'form': form
    }
    return render(request, 'propose_puzzle.html', context=context)


def about_app(request):
    return HttpResponse('About app')
