from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('movie/<slug:slug>/', views.movie_detail, name='movie_detail'),
]