from django.db import models

# Create your models here.
# urgences/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone
from patients.models import Patient
from personnel.models import PersonnelMedical

class PassageUrgence(models.Model):
    GRAVITE_CHOICES = [
        ('faible', 'Faible'),
        ('moyenne', 'Moyenne'),
        ('grave', 'Grave'),
        ('critique', 'Critique'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_arrivee = models.DateTimeField(default=timezone.now)
    motif = models.CharField(max_length=255)
    gravite = models.CharField(max_length=20, choices=GRAVITE_CHOICES)
    prise_en_charge = models.TextField(blank=True)
    oriente_vers = models.CharField(max_length=100, blank=True)
    medecin_responsable = models.ForeignKey(PersonnelMedical, on_delete=models.SET_NULL, null=True, blank=True)
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.patient.nom_complet} - {self.date_arrivee.strftime('%d/%m/%Y %H:%M')}"

class HistoriqueUrgence(models.Model):
    passage = models.ForeignKey(PassageUrgence, on_delete=models.CASCADE, related_name='historiques')
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    date_action = models.DateTimeField(default=timezone.now)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.action} - {self.passage.patient} - {self.date_action.strftime('%d/%m/%Y %H:%M')}"

from django.db import models
from patients.models import Patient

class Urgence(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    motif = models.CharField(max_length=255)
    date_arrivee = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Urgence de {self.patient.nom_complet()} - {self.date_arrivee.strftime('%d/%m/%Y')}"
