from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Movie(models.Model):
    title = models.CharField(verbose_name='Title', max_length=255, unique=True)
    recommended = models.BooleanField(default=False, verbose_name='Recommended')
    picture = models.ImageField(verbose_name='Picture from the movie', upload_to='media/picture')

    ets = models.BooleanField(default=True, verbose_name='Estado')
    cre = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='mod_usr')

    def __str__(self):
        return f'[{self.title}] - {self.ets}'

    class Meta:
        ordering = ['title']
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'


class Users(AbstractUser):
    pro = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Responsable',
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        ordering = ['username']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.get_full_name()}'
