from django import forms
from .models import PersonnelMedical

class PersonnelForm(forms.ModelForm):
    class Meta:
        model = PersonnelMedical
        fields = '__all__'
        widgets = {
            'date_embauche': forms.DateInput(attrs={'type': 'date'}),
        }
