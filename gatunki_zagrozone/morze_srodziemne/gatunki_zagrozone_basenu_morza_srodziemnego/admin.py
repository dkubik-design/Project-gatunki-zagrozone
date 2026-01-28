#Część kody wpełni wygenerowna przez chat

from django.contrib import admin
from .models import Continent, Country, Species

@admin.register(Continent)
class ContinentAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'continent', 'domain_code') # Kolumny w tabeli
    list_filter = ('continent',) # Filtr po prawej stronie
    search_fields = ('name',) # Wyszukiwarka

@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    # Co widzimy na liście gatunków
    list_display = ('name_pl', 'name_lat', 'category_ckgz', 'is_endemic')
    # Filtry, które ułatwią Ci życie
    list_filter = ('category_ckgz', 'is_endemic', 'protection_actions')
    # Wyszukiwanie po nazwach polskich i łacińskich
    search_fields = ('name_pl', 'name_lat')
    # Grupowanie pól w formularzu edycji (opcjonalne, ale bardzo czytelne)
    fieldsets = (
        ('Podstawowe informacje', {
            'fields': ('name_pl', 'name_lat', 'category_ckgz')
        }),
        ('Systematyka', {
            'fields': ('kingdom', 'phylum', 'species_class', 'order', 'family', 'genus')
        }),
        ('Ochrona i status', {
            'fields': ('protection_actions', 'protection_intensity', 'protection_organizations', 'is_endemic', 'is_mainstream')
        }),
        ('Opisy', {
            'fields': ('description', 'appearance', 'habitat_and_diet')
        }),
        ('Lokalizacja', {
            'fields': ('countries',)
        }),
    )