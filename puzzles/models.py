from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from django.template.defaultfilters import slugify


class CommonPuzzle(models.Model):
    """Abstract model for tables"""
    title = models.CharField('Title', max_length=100, db_index=True)
    slug = models.SlugField('URL', max_length=100, unique=True, db_index=True)
    question = models.TextField('Question')
    answer = models.TextField('Answer')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('puzzle', kwargs={'puzzle_slug': self.slug})

    # def get_comment(self):
    #     return self.comment_set.filter(parent__isnull=False).select_related('user')

    class Meta:
        abstract = True


class Puzzle(CommonPuzzle):
    """Puzzle model"""

    class Meta:
        verbose_name = 'Puzzle'
        verbose_name_plural = 'Puzzles'
        ordering = ['id']


class UserPuzzle(CommonPuzzle):
    """UserPuzzle model"""
    draft = models.BooleanField('Draft', default=True)
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)

    # Generate slug in form
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(UserPuzzle, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'User Puzzle'
        verbose_name_plural = 'Users Puzzles'
        ordering = ['id']


class Comment(models.Model):
    """Comment"""
    text = models.TextField('Comment', max_length=5000)
    parent = models.ForeignKey('self', verbose_name='parent', on_delete=models.SET_NULL, blank=True, null=True)
    puzzle = models.ForeignKey(Puzzle, verbose_name='puzzle', on_delete=models.CASCADE, blank=True, null=True)
    user_puzzle = models.ForeignKey(UserPuzzle, verbose_name='user_puzzle', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, verbose_name='user', on_delete=models.SET_DEFAULT, default='Unknown user')

    def __str__(self):
        if self.puzzle:
            return f"{self.user} - {self.puzzle}"
        else:
            return f"{self.user} - {self.user_puzzle}"

    def get_child_comments(self):
        return self.comment_set.filter(parent__isnull=False).select_related('user')

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ['-id']


class PageHit(models.Model):
    """Number of clicks per page"""
    url = models.CharField(max_length=255, unique=True)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.url} - {self.count}'

    class Meta:
        verbose_name = 'Page hit'
        verbose_name_plural = 'Page hits'
        ordering = ['-count']


