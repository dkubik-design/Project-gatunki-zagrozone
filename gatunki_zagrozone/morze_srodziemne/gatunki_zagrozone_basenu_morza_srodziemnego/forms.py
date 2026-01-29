from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['imie', 'nazwisko', 'plec', 'wiek', 'organizacja', 'opis']
        widgets = {
            'wiek': forms.NumberInput(attrs={'min': '0', 'max': '99', 'step': '1'}),
        }
    def clean_wiek(self):
        wiek = self.cleaned_data.get('wiek')
        if wiek < 0 or wiek > 99:
            raise forms.ValidationError("Podaj realny wiek!")
        return wiek

