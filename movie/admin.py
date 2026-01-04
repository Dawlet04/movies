from django.contrib import admin
from django.utils.html import format_html
from .models import Countries, CustomUser, Actors, Genres, Movie, Comment


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['avatar_preview', 'username', 'email', 'phone_num', 'card_number', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    search_fields = ['username', 'email', 'phone_num']
    readonly_fields = ['avatar_large', 'date_joined', 'last_login']
    
    def avatar_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;"/>',
                obj.photo.url
            )
        return "👤"
    avatar_preview.short_description = 'Аватар'
    
    def avatar_large(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-width: 250px; border-radius: 16px;"/>', obj.photo.url)
        return "Нет фото"
    avatar_large.short_description = 'Фото'


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = ['genre', 'slug']
    search_fields = ['genre']
    prepopulated_fields = {'slug': ('genre',)}


@admin.register(Actors)
class ActorsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'slug']
    search_fields = ['full_name']
    prepopulated_fields = {'slug': ('full_name',)}


@admin.register(Countries)
class CountriesAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'year', 'age']
    list_filter = ['year', 'age', 'genres', 'counries']
    search_fields = ['title', 'description']
    filter_horizontal = ['genres', 'actors', 'counries']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'text_preview', 'created_at']
    list_filter = ['created_at', 'movie']
    search_fields = ['userusername', 'movietitle', 'text']
    readonly_fields = ['created_at']
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Текст'


admin.site.site_header = '🎬 Админ-панель Кинопортала'
admin.site.site_title = 'Кинопортал Admin'
admin.site.index_title = 'Панель управления'