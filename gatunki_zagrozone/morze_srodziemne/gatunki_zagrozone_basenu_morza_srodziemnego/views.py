from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')
    
def dodaj_gatunek(request):
    return HttpResponse("Tu będzie formularz dodawania gatunku!")

def zaloguj(request):
    return HttpResponse("tu będzie formularz logowania")

def profil(request):
    return HttpResponse("tu będzie profil")

    