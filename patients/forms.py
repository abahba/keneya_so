from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # 1. Masquer les champs en fonction du statut
        statut = self.instance.statut if self.instance else None

        if statut != 'sorti':
            self.fields['date_sortie'].widget = forms.HiddenInput()
            self.fields['signature_sortie'].widget = forms.HiddenInput()

        if statut != 'décédé':
            self.fields['date_deces'].widget = forms.HiddenInput()
            self.fields['signature_deces'].widget = forms.HiddenInput()

        # 2. Restreindre modification aux médecins/infirmiers
        if user and user.role not in ['medecin', 'infirmier']:
            for field in ['statut', 'date_sortie', 'signature_sortie', 'date_deces', 'signature_deces']:
                if field in self.fields:
                    self.fields[field].disabled = True

    class Meta:
        model = Patient
        fields = [
            'nom', 'prenom', 'date_naissance', 'sexe', 'adresse', 'telephone',
            'statut', 'date_sortie', 'signature_sortie', 'date_deces', 'signature_deces'
        ]
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'date_sortie': forms.DateInput(attrs={'type': 'date'}),
            'date_deces': forms.DateInput(attrs={'type': 'date'}),
        }

