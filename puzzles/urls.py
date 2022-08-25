from django.urls import path
from .views import *

urlpatterns = [
    path('', main_puzzles, name='home'),
    path('', main_puzzles, name='main_puzzles'),
    path('puzzle/<slug:puzzle_slug>/', puzzle_detail, name='puzzle'),
    path('users_puzzles/', users_puzzles, name='users_puzzles'),
    path('user_puzzle/<slug:user_puzzle_slug>/', user_puzzle_detail, name='user_puzzle'),

    path('sign_in/', sign_in, name='sign_in'),
    path('sign_up/', sign_up, name='sign_up'),

    path('propose_puzzle/', propose_puzzle, name='propose_puzzle'),
    path('about_app/', propose_puzzle, name='about_app'),
]
