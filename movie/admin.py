from django.contrib import admin
from .models import Countries,CustomUser,Actors,Genres,Movie



@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone_num', 'card_number')
    search_fields = ('username', 'phone_num')
    list_filter = ('is_staff', 'is_superuser')


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('genre',)}
    list_display = ('genre', 'slug')
    search_fields = ('genre',)


@admin.register(Actors)
class ActorsAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'slug')
    search_fields = ('full_name',)
    prepopulated_fields = {'slug': ('full_name',)}


@admin.register(Countries)
class CountriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'age')
    search_fields = ('title',)
    list_filter = ('year', 'genres', 'counries')
    filter_horizontal = ('genres', 'actors', 'counries')
    prepopulated_fields = {'slug': ('title',)}