from django.conf.urls.static import static
from django.urls import path, include, re_path

from app import settings
from .views import *
from .api_views import *

urlpatterns = [
    path('', main_puzzles, name='home'),
    path('profile', user_profile, name='profile'),
    path('profile/edit', user_edit_profile, name='profile_edit'),
    path('', main_puzzles, name='main_puzzles'),
    path('puzzle/<slug:puzzle_slug>/', puzzle_detail, name='puzzle'),
    path('users_puzzles/', users_puzzles, name='users_puzzles'),
    path('propose_puzzle/', propose_puzzle, name='propose_puzzle'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('sign_in/', SignInView.as_view(), name='signin'),
    path('logout/', logout_user, name='logout'),
    path('about_app/', about_app, name='about_app'),

    # api urls
    path('api/v1/puzzleslist/', PuzzleAPIList.as_view()),
    path('api/v1/puzzle/detail/<int:pk>/', PuzzleAPIDetail.as_view()),
    path('api/v1/userpuzzlelist/', UserPuzzleAPIList.as_view()),
    path('api/v1/userpuzzle/detail/<int:pk>/', UserPuzzleAPIDetail.as_view()),
    path('api/v1/userpuzzle/create/', UserPuzzleAPICreate.as_view()),
    # authentication
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/v1/auth/', include('djoser.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

