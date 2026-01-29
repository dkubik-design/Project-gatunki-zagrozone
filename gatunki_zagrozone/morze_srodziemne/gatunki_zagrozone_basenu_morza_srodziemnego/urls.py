from django.urls import path
from . import views  # To zadziała, bo views.py jest w tym samym folderze

urlpatterns = [
    path('', views.home, name='home'),
]

