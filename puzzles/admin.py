from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .models import *
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'phone', 'gender', 'birth_date', 'get_photo']
    list_display_links = ('username',)
    search_fields = ('username',)
    ordering = ('-id',)

    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            'Custom fields',
            {
                'fields': (
                    'phone',
                    'gender',
                    'birth_date',
                    'photo',
                )
            }
        )
    )

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom fields',
            {
                'fields': (
                    'phone',
                    'gender',
                    'birth_date',
                    'photo',
                )
            }
        )
    )

    def get_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_photo.short_description = 'Photo'


@admin.register(Puzzle)
class PuzzleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'question', 'answer')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-id',)


@admin.register(UserPuzzle)
class UserPuzzleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'question', 'answer', 'draft', 'user')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'user')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-id',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'puzzle', 'user_puzzle', 'user', 'parent')
    list_display_links = ('id', 'puzzle', 'user_puzzle')
    search_fields = ('text', 'user', 'parent')
    ordering = ('-id',)


@admin.register(PageHit)
class PageHitAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'count')

