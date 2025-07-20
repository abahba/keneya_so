from django import forms
from .models import ExamenImagerie

class ExamenImagerieForm(forms.ModelForm):
    class Meta:
        model = ExamenImagerie
        fields = ['patient', 'consultation', 'type_imagerie', 'description', 'fichier_resultat', 'prescripteur']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
