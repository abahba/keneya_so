from django import forms
from .models import OperationChirurgicale
from personnel.models import PersonnelMedical

class OperationChirurgicaleForm(forms.ModelForm):
    class Meta:
        model = OperationChirurgicale
        fields = '__all__'
        widgets = {
            'date_operation': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'compte_rendu': forms.Textarea(attrs={'rows': 4}),
            'observations': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtre pour n'afficher que le personnel médical actif
        self.fields['chirurgien'].queryset = PersonnelMedical.objects.filter(actif=True)
        self.fields['anesthesiste'].queryset = PersonnelMedical.objects.filter(actif=True)

class HistoriqueOperationFilterForm(forms.Form):
    action = forms.CharField(label="Action", required=False)
    utilisateur = forms.CharField(label="Utilisateur", required=False)
    date_debut = forms.DateField(label="Date début", required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_fin = forms.DateField(label="Date fin", required=False, widget=forms.DateInput(attrs={'type': 'date'}))
