from django import forms
from .models import MembreAdministratif

class MembreAdministratifForm(forms.ModelForm):
    class Meta:
        model = MembreAdministratif
        fields = '__all__'

class MembreAdministratifFilterForm(forms.Form):
    nom = forms.CharField(label="Nom", required=False)
    fonction = forms.CharField(label="Fonction", required=False)
    actif = forms.ChoiceField(
        label="Actif",
        required=False,
        choices=[('', 'Tous'), ('oui', 'Oui'), ('non', 'Non')],
    )
