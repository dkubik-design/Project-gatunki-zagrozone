from django.db import models
from django.core.exceptions import ValidationError

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
    
    countries = models.ManyToManyField(Country, verbose_name="Kraje występowania")

    def clean(self):
        if self.protection_actions:
            if not self.protection_intensity:
                raise ValidationError({'protection_intensity': "Jeśli działania są prowadzone, musisz określić ich intensywność!"})
            if not self.protection_organizations:
                raise ValidationError({'protection_organizations': "Podaj nazwy organizacji!"})

    def __str__(self):
        return f"{self.name_pl} ({self.name_lat})"







