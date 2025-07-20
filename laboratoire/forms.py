from django import forms
from .models import AnalyseBiologique, ResultatAnalyse

class AnalyseBiologiqueForm(forms.ModelForm):
    class Meta:
        model = AnalyseBiologique
        fields = ['patient', 'type_analyse', 'date_prescription', 'date_demande']
        # Vous pouvez personnaliser les widgets si nécessaire
        widgets = {
            'date_demande': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'date_prescription': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        type_analyse = cleaned_data.get("type_analyse")
        autre = cleaned_data.get("autre_type_analyse")

        if not type_analyse and not autre:
            raise forms.ValidationError("Vous devez choisir un type d’analyse ou en écrire un nouveau.")
        return cleaned_data


class ResultatAnalyseForm(forms.ModelForm):
    class Meta:
        model = ResultatAnalyse
        fields = '__all__'  # Inclut tous les champs du modèle
        widgets = {
            'contenu': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }
