from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import generate_unique_slug



class CustomUser(AbstractUser):
    phone_num = models.CharField(max_length=13, help_text='+998XXXXXXX')
    photo = models.ImageField(upload_to='users/')
    card_number = models.CharField(max_length=16, help_text='9860yyyyxxxx0101',
                                   blank=True, null=True)
    
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'



class Genres(models.Model):
    genre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, 'genre')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.genre
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'




class Actors(models.Model):
    full_name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, blank=True)
    biography = models.TextField()
    image = models.ImageField(upload_to='actors/')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, 'full_name')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
    class Meta:
        verbose_name = 'Актер'
        verbose_name_plural = 'Актеры'



class Countries(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, 'name')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'



class Movie(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='posters/')
    year = models.CharField(max_length=4, help_text='ГГГГ')
    description = models.TextField()
    counries = models.ManyToManyField(Countries)
    genres = models.ManyToManyField(Genres)
    actors = models.ManyToManyField(Actors)
    age = models.CharField(max_length=3, default='16+')
    time = models.CharField(max_length=3)
    trailer = models.URLField()
    film = models.FileField(upload_to='films/')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, 'title')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name=  'Фильм'
        verbose_name_plural  = 'Фильмы'


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']  # Новые комментарии первыми
    
    def __str__(self):
        return f'{self.user.username} - {self.movie.title}'