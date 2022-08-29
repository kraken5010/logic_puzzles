from django.contrib import admin

from .models import *


class PuzzleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'question', 'answer')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


class UserPuzzleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'question', 'answer', 'draft', 'user')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'user')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Puzzle, PuzzleAdmin)
admin.site.register(UserPuzzle, UserPuzzleAdmin)
