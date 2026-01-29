from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponse
from .forms import ProfileForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def home(request):
    return render(request, 'home.html')
    
def dodaj_gatunek(request):
    return HttpResponse("Tu będzie formularz dodawania gatunku!")

def profil(request):
    return HttpResponse("tu będzie profil")

def zaloguj(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def zarejestruj(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, f"Twoje konto: {user.username} zostało poprawnie utworzone")
            return redirect('login_url')
    else:
        user_form = UserCreationForm()
        profile_form = ProfileForm()
    
    return render(request, 'register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def wyloguj(request):
    logout(request)
    return redirect('home')


