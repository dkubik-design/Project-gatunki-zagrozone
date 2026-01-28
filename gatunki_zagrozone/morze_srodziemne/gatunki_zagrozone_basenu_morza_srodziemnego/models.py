from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone


#Obszar

def validate_continent_name(value):
    allowed = ['Europa', 'Azja', 'Afryka']
    if value.capitalize() not in allowed:
        raise ValidationError(f"{value} Błąd")

class Continent(models.Model):
    name = models.CharField(max_length=20, validators=[validate_continent_name], unique=True)
    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=40, unique=True)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)
    domain_code = models.CharField(max_length=5)

    def clean(self):
        valid_data = {
            'Europa': ['Albania', 'Chorwacja', 'Czarnogóra', 'Francja', 'Grecja', 
                       'Hiszpania', 'Monako', 'Słowenia', 'Włochy', 'Malta'],
            'Azja': ['Cypr', 'Izrael', 'Liban', 'Syria', 'Turcja'],
            'Afryka': ['Algieria', 'Egipt', 'Libia', 'Maroko', 'Tunezja']
        }
        country_name_capitalized = self.name.capitalize()
        cont_name = self.continent.name 

        if cont_name in valid_data:
            if country_name_capitalized not in valid_data[cont_name]:
                raise ValidationError(f"Błąd: {self.name} tego kraju nie ma na kontynencie {cont_name}!")
            self.name = country_name_capitalized

    def __str__(self):
        return self.name

#Gatunki

class Species(models.Model):
    CKGZ_CATEGORIES = [
        ('LC', 'LC - Najmniejszej troski'),
        ('NT', 'NT - Bliskie zagrożenia'),
        ('VU', 'VU - Narażony'),
        ('EN', 'EN - Zagrożony'),
        ('CR', 'CR - Krytycznie zagrożony'),
        ('EW', 'EW - Wymarły na wolności'),
    ]

    INTENSITY_CHOICES = [
        ('low', 'Niska'),
        ('medium', 'Średnia'),
        ('high', 'Wysoka'),
    ]

    ENDEMIT_CHOICES = [
        ('tak', 'Endemit'),
        ('nie', 'Gatunek o dużej powierzchni występowania'),
    ]

    MAINSTREAM_CHOICES = [
        ('tak', 'Gatunek mainstreamowy'),
        ('nie', 'Gatunek nieznany szerszej publice'),
    ]


    name_pl = models.CharField(max_length=100, default="N/A", verbose_name="Nazwa polska")
    name_lat = models.CharField(max_length=100, verbose_name="Nazwa łacińska")
    
    category_ckgz = models.CharField(max_length=2, choices=CKGZ_CATEGORIES, verbose_name="Kategoria CKGZ")

    kingdom = models.CharField(max_length=100, verbose_name="Królestwo")
    phylum = models.CharField(max_length=100, verbose_name="Typ")
    species_class = models.CharField(max_length=100, verbose_name="Gromada")
    order = models.CharField(max_length=100, verbose_name="Rząd")
    family = models.CharField(max_length=100, verbose_name="Rodzina")
    genus = models.CharField(max_length=100, verbose_name="Rodzaj")

    protection_actions = models.BooleanField(default=False, verbose_name="Działania prowadzone?")
    protection_intensity = models.CharField(max_length=10, choices=INTENSITY_CHOICES, blank=True, null=True)
    protection_organizations = models.TextField(blank=True, null=True, verbose_name="Organizacje")

    is_endemic = models.CharField(max_length=3, choices=ENDEMIT_CHOICES, default='nie')
    is_mainstream = models.CharField(max_length=3, choices=MAINSTREAM_CHOICES, default='nie')

    description = models.TextField(verbose_name="Opis")
    appearance = models.TextField(verbose_name="Wygląd")
    habitat_and_diet = models.TextField(verbose_name="Habitat i dieta")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data dodania do bazy")
    
    countries = models.ManyToManyField(Country, verbose_name="Kraje występowania")

    author = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Autor wpisu"
    )

    def clean(self):
        if self.protection_actions:
            if not self.protection_intensity:
                raise ValidationError({'protection_intensity': "Jeśli działania są prowadzone, musisz określić ich intensywność!"})
            if not self.protection_organizations:
                raise ValidationError({'protection_organizations': "Podaj nazwy organizacji!"})

    def __str__(self):
        return f"{self.name_pl} ({self.name_lat})"




####


class Profile(models.Model):
    class Plec(models.IntegerChoices):
        KOBIETA = 1, 'Kobieta'
        MEZCZYZNA = 2, 'Mężczyzna'
        NIE_PODAJE = 3, 'Nie chcę podawać'


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    

    imie = models.CharField(max_length=20, blank=False)
    nazwisko = models.CharField(max_length=20, blank=False)
    plec = models.IntegerField(choices=Plec.choices, default=Plec.NIE_PODAJE)
    wiek = models.IntegerField(null=False, blank=False)
    organizacja = models.TextField(blank=True, null=True, verbose_name="Działa w organizacji")
    opis = models.TextField(blank=True, null=True, verbose_name="Kilka słów o sobie")
    
    
    data_utworzenia = models.DateTimeField(default=timezone.now)

    def get_ranga(self):
        count = self.user.species_set.count()
        
        if count >= 100:
            return "Aktywista Terrorysta"
        elif count >= 50:
            return "Przyjaciel Natury"
        elif count >= 10:
            return "E-kolog"
        elif count >= 1:
            return "Ekolog"
        else:
            return "Nowicjusz"

    def __str__(self):
        return f"Profil użytkownika {self.user.username}"













