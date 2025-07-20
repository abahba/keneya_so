from django import forms
from .models import Consultation
from .models import DossierMedical
from .models import Ordonnance, LigneOrdonnance
from django.forms import inlineformset_factory
from .models import Hospitalisation
from .models import PrescriptionAnalyse

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['patient', 'symptomes', 'diagnostic', 'traitement', 'notes']
        widgets = {
            'symptomes': forms.Textarea(attrs={'rows': 3}),
            'diagnostic': forms.Textarea(attrs={'rows': 3}),
            'traitement': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

class DossierMedicalForm(forms.ModelForm):
    class Meta:
        model = DossierMedical
        fields = ['antecedents', 'allergies', 'traitements_en_cours', 'autres_infos']

class OrdonnanceForm(forms.ModelForm):
    class Meta:
        model = Ordonnance
        fields = ['type_assurance']

LigneOrdonnanceFormSet = inlineformset_factory(
    Ordonnance,
    LigneOrdonnance,
    fields=('medicament', 'quantite', 'posologie', 'duree'),
    extra=1,
    can_delete=True
)

class HospitalisationForm(forms.ModelForm):
    class Meta:
        model = Hospitalisation
        fields = ['patient', 'service', 'date_entree', 'date_sortie', 'motif', 'medecin_responsable']
        widgets = {
            'motif': forms.Textarea(attrs={'rows': 3}),
            'date_entree': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'date_sortie': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class PrescriptionAnalyseForm(forms.ModelForm):
    class Meta:
        model = PrescriptionAnalyse
        fields = ['type_analyse', 'autre_type_analyse']
