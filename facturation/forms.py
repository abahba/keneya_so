from django import forms
from .models import Facture, Paiement
from .models import Remboursement

class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['patient', 'ordonnance', 'montant_total']

class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = ['facture', 'montant_verse', 'mode_paiement']

class RemboursementForm(forms.ModelForm):
    class Meta:
        model = Remboursement
        fields = ['paiement', 'montant', 'motif']
        widgets = {
            'motif': forms.Textarea(attrs={'rows': 2}),
        }
