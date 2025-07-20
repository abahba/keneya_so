from django import forms
from .models import Assurance, PatientAssure, PriseEnCharge

class AssuranceForm(forms.ModelForm):
    class Meta:
        model = Assurance
        fields = '__all__'

class PatientAssureForm(forms.ModelForm):
    class Meta:
        model = PatientAssure
        fields = '__all__'

class PriseEnChargeForm(forms.ModelForm):
    class Meta:
        model = PriseEnCharge
        fields = '__all__'
