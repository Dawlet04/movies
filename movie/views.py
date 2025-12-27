from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Movie, Genres, Countries, Actors
from .forms import CustomUserRegistrationForm, MovieSearchForm, MovieFilterForm, ProfileEditForm
from django.contrib.auth.decorators import login_required


def home(request):
    movies = Movie.objects.all()
    
    search_form = MovieSearchForm(request.GET or None)
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        if query:
            movies = movies.filter(Q(title__icontains=query)|Q(description__icontains=query))
    

    filter_form = MovieFilterForm(request.GET or None)
    if filter_form.is_valid():
        data = filter_form.cleaned_data
        
        if data.get('genre'):
            movies = movies.filter(genres=data['genre'])
        if data.get('country'):
            movies = movies.filter(counries=data['country'])  
        if data.get('age'):
            movies = movies.filter(age=data['age'])
        if data.get('sort_by'):
            movies = movies.order_by(data['sort_by'])
    
 
    paginator = Paginator(movies, 12)
    page_number = request.GET.get('page', 1)  
    movies_page = paginator.get_page(page_number)  
    
    context = {
        'movies': movies_page,
        'total_movies': paginator.count,  
        'search_form': search_form,
        'filter_form': filter_form,
    }
    
    return render(request, 'films/home.html', context)


def register(request):
    form = CustomUserRegistrationForm(request.POST or None, request.FILES or None)
    
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')
    
    return render(request, 'films/register.html', {'form': form})


def movie_detail(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    related_movies = Movie.objects.filter(
        genres__in=movie.genres.all()
    ).exclude(id=movie.id).distinct()[:6]
    
    return render(request, 'films/detail.html', {
        'movie': movie,
        'related_movies': related_movies
    })

def actors(request, slug):
    actor = get_object_or_404(Actors, slug=slug)
    movies = actor.movie_set.all()  # Фильмы с этим актёром
    
    return render(request, 'films/actors.html', {
        'actor': actor,
        'movies': movies,  # Опционально, если хотите отдельно
    })


@login_required
def profile(request):
    """Страница профиля пользователя"""
    user = request.user
    
    context = {
        'user': user,
    }
    
    return render(request, 'films/profile.html', context)


@login_required
def profile_edit(request):
    """Редактирование профиля"""
    user = request.user
    
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=user)
    
    return render(request, 'films/profile_edit.html', {'form': form})