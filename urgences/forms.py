# urgences/forms.py

from django import forms
from .models import PassageUrgence
from django.utils import timezone

class PassageUrgenceForm(forms.ModelForm):
    class Meta:
        model = PassageUrgence
        fields = [
            'patient', 'motif', 'gravite', 'prise_en_charge',
            'oriente_vers', 'medecin_responsable'
        ]
        widgets = {
            'prise_en_charge': forms.Textarea(attrs={'rows': 3}),
        }

class HistoriqueUrgenceFilterForm(forms.Form):
    action = forms.CharField(required=False, label='Action')
    utilisateur = forms.CharField(required=False, label='Utilisateur')
    date_debut = forms.DateField(required=False, label='Date de début', widget=forms.DateInput(attrs={'type': 'date'}))
    date_fin = forms.DateField(required=False, label='Date de fin', widget=forms.DateInput(attrs={'type': 'date'}))

from django import forms

class UrgenceFilterForm(forms.Form):
    type_urgence = forms.CharField(label="Type d'urgence", required=False)
    utilisateur = forms.CharField(label="Utilisateur", required=False)
    date_debut = forms.DateField(label="Du", required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_fin = forms.DateField(label="Au", required=False, widget=forms.DateInput(attrs={'type': 'date'}))
