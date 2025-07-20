from django import forms
from .models import ParametresSysteme

class ParametresSystemeForm(forms.ModelForm):
    class Meta:
        model = ParametresSysteme
        fields = '__all__'
