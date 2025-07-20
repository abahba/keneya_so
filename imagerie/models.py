from django.db import models

# Create your models here.
from django.db import models
from patients.models import Patient
from consultations.models import Consultation
from django.contrib.auth import get_user_model

User = get_user_model()

class TypeImagerie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class ExamenImagerie(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    consultation = models.ForeignKey(Consultation, on_delete=models.SET_NULL, null=True, blank=True)
    type_imagerie = models.ForeignKey(TypeImagerie, on_delete=models.CASCADE)
    date_prescription = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    fichier_resultat = models.FileField(upload_to='resultats_imagerie/', blank=True, null=True)
    prescripteur = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    related_name='examens_prescrits'
)

    utilisateur = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='examens_enregistres'
)

    def __str__(self):
        return f"{self.type_imagerie.nom} - {self.patient.nom} ({self.date_prescription.date()})"

class HistoriqueImagerie(models.Model):
    ACTIONS = [
        ('ajout', 'Ajout'),
        ('modification', 'Modification'),
        ('suppression', 'Suppression'),
    ]

    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTIONS)
    date_action = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.utilisateur} - {self.action} - {self.patient} ({self.date_action.strftime('%d/%m/%Y %H:%M')})"
