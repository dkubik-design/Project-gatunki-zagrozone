from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-species/', views.dodaj_gatunek, name='add_species_url'),
    path('login/', views.zaloguj, name='login_url'),
    path('profile/', views.profil, name='profile_url'),
]

