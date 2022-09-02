from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import *
from .decorators import counted

menu = [
    {'title': 'Puzzles', 'url_name': 'main_puzzles'},
    {'title': 'Users puzzles', 'url_name': 'users_puzzles'},
    {'title': 'Propose a puzzle', 'url_name': 'propose_puzzle'},
    {'title': 'About app', 'url_name': 'about_app'}
]


def user_profile(request):
    """Profile user"""
    user = CustomUser.objects.get(username=request.user)

    context = {
        'menu': menu,
        'title': f'Profile: {request.user.username}',
        'user': user,
        'phone': request.user.phone
    }
    return render(request, 'profile.html', context=context)


def user_edit_profile(request):
    """Edit profile user"""
    if request.method == 'POST':
        user_form = CustomUserProfileEdit(instance=request.user, data=request.POST, files=request.FILES)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = CustomUserProfileEdit(instance=request.user)

    context = {
        'menu': menu,
        'title': f'Edit profile: {request.user.username}',
        'form': user_form,
        'user_photo': request.user.photo
    }
    return render(request, 'profile_edit.html', context=context)


# Main page
def main_puzzles(request):
    """Main puzzles for page list"""
    puzzles = Puzzle.objects.all()
    context = {
        'menu': menu,
        'title': 'Logic puzzles',
        'puzzles': puzzles
    }
    return render(request, 'main_puzzles.html', context=context)


@counted
def puzzle_detail(request, puzzle_slug):
    """Puzzle detail page"""
    try:
        puzzle = Puzzle.objects.get(slug=puzzle_slug)
        try:
            next_puzzle = Puzzle.objects.get(pk=int(puzzle.id + 1))
        except:
            next_puzzle = None
        try:
            prev_puzzle = Puzzle.objects.get(pk=int(puzzle.id - 1))
        except:
            prev_puzzle = None

        puzzle_to_form = puzzle
        comments = Comment.objects.filter(puzzle=puzzle, parent__isnull=True).select_related('user')

    except:
        puzzle = UserPuzzle.objects.get(slug=puzzle_slug)
        try:
            next_puzzle = UserPuzzle.objects.get(pk=int(puzzle.id + 1))
        except:
            next_puzzle = None
        try:
            prev_puzzle = UserPuzzle.objects.get(pk=int(puzzle.id - 1))
        except:
            prev_puzzle = None

        user_puzzle_to_form = puzzle
        comments = Comment.objects.filter(user_puzzle=puzzle, parent__isnull=True).select_related('user')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            try: data.puzzle = puzzle_to_form
            except: data.puzzle = None
            try: data.user_puzzle = user_puzzle_to_form
            except: data.user_puzzle = None

            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))

            form.save()
            return HttpResponseRedirect(request.path)
    else:
        form = CommentForm()

    num_of_transition = PageHit.objects.filter(url=request.path).values('count')

    context = {
        'menu': menu,
        'puzzle': puzzle,
        'comments': comments,
        'title': puzzle.title,
        'next_puzzle': next_puzzle,
        'prev_puzzle': prev_puzzle,
        'form': form,
        'count': num_of_transition[0]['count']
    }
    return render(request, 'puzzle_detail.html', context=context)


def users_puzzles(request):
    """Users puzzles list to page"""
    users_puzzles = UserPuzzle.objects.filter(draft=True)
    context = {
        'menu': menu,
        'title': 'Users puzzles',
        'users_puzzles': users_puzzles
    }
    return render(request, 'users_puzzles.html', context=context)


def propose_puzzle(request):
    """Users propose their puzzle"""
    if request.method == 'POST':
        form = AddUserPuzzleForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            form.save()
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
    """About app page"""
    context = {
        'menu': menu,
        'title': 'About app',
    }
    return render(request, 'about_app.html', context=context)


class SignUpView(CreateView):
    """Authorization"""
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        context = {
            'menu': menu,
            'title': 'Sign up',
            'form': self.form_class
        }
        return context

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, self.template_name, {'form': form})


class SignInView(LoginView):
    """Authentication"""
    form_class = SignInForm
    template_name = 'signin.html'

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
    return redirect('signin')


