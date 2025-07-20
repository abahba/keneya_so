from django import forms
from .models import Medicament

class MedicamentForm(forms.ModelForm):
    class Meta:
        model = Medicament
        fields = '__all__'
