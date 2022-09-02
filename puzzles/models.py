import re
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError

from pytils import translit


def validate_phone(phone):
    """Phone number validator"""
    regex_ua = r'^\+380\d{9}$'
    if not re.match(regex_ua, phone):
        raise ValidationError(f'{phone} is not valid!')


class CustomUser(AbstractUser):
    """Custom User model"""
    GENDERS = (
        ('male', 'male'),
        ('female', 'female')
    )

    phone = models.CharField('Phone', validators=[validate_phone], help_text='format +380xxxxxxxxx', max_length=13, blank=True, null=True)
    gender = models.CharField('Gender', max_length=6, choices=GENDERS, default='')
    birth_date = models.DateField('Birth date', default='2000-12-31')
    photo = models.ImageField('Photo', upload_to='user_photo/', blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


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
    user = models.ForeignKey(CustomUser, verbose_name='User', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """Slug generation from cyrillic"""
        self.slug = translit.slugify(self.title)
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
    user = models.ForeignKey(CustomUser, verbose_name='user', on_delete=models.SET_DEFAULT, default='Unknown user')

    def __str__(self):
        if self.puzzle:
            return f"{self.user} - {self.puzzle}"
        else:
            return f"{self.user} - {self.user_puzzle}"

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


