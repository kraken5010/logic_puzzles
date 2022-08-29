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

    class Meta:
        abstract = True


class Puzzle(CommonPuzzle):
    """Puzzle model"""
    def get_absolute_url(self):
        return reverse('puzzle', kwargs={'puzzle_slug': self.slug})

    class Meta:
        verbose_name = 'Puzzle'
        verbose_name_plural = 'Puzzles'
        ordering = ['id']


class UserPuzzle(CommonPuzzle):
    """UserPuzzle model"""
    draft = models.BooleanField('Draft', default=True)
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('user_puzzle', kwargs={'user_puzzle_slug': self.slug})

    # Generate slug in form
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(UserPuzzle, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'User Puzzle'
        verbose_name_plural = 'Users Puzzles'
        ordering = ['id']
