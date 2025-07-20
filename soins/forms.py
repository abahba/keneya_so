from django import forms
from .models import Soin, HistoriqueSoin
from accounts.models import CustomUser


class SoinForm(forms.ModelForm):
    class Meta:
        model = Soin
        exclude = ['date_soin', 'utilisateur']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'type_soin': forms.Select(attrs={'class': 'form-select'}),
        }


class HistoriqueSoinFilterForm(forms.Form):
    patient = forms.CharField(label="Nom du patient", required=False)
    type_soin = forms.ChoiceField(
        label="Type de soin",
        choices=[('', 'Tous')] + list(Soin.TYPE_SOIN_CHOICES),
        required=False
    )
    action = forms.ChoiceField(
        label="Action",
        choices=[('', 'Toutes')] + list(HistoriqueSoin.ACTIONS),
        required=False
    )
    utilisateur = forms.ModelChoiceField(
        label="Utilisateur",
        queryset=CustomUser.objects.all(),
        required=False
    )
    date_debut = forms.DateField(
        label="Date début",
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    date_fin = forms.DateField(
        label="Date fin",
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

