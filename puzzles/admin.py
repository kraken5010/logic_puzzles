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


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'puzzle', 'user_puzzle', 'user', 'parent')
    list_display_links = ('id', 'puzzle', 'user_puzzle')
    search_fields = ('text', 'user', 'parent')


class PageHitAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'count')


admin.site.register(Puzzle, PuzzleAdmin)
admin.site.register(UserPuzzle, UserPuzzleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(PageHit, PageHitAdmin)
