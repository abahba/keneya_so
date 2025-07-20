from django.db import models

# Create your models here.
import uuid
from django.db import models

class Patient(models.Model):
    numero_dossier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    sexe = models.CharField(max_length=10)
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)

    # Champs pour statut
    statut = models.CharField(max_length=20, choices=[('consulté', 'Consulté'), ('hospitalisé', 'Hospitalisé'), ('sorti', 'Sorti'), ('décédé', 'Décédé')], default='consulté')
    date_sortie = models.DateField(null=True, blank=True)
    signature_sortie = models.CharField(max_length=100, blank=True)
    date_deces = models.DateField(null=True, blank=True)
    signature_deces = models.CharField(max_length=100, blank=True)

    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)


    actif = models.BooleanField(default=True)  # Champ pour désactivation (soft delete)

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.numero_dossier}"
from django.utils import timezone
from django.conf import settings

class HistoriquePatient(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='historiques')
    action = models.CharField(max_length=255)  # ex: 'création', 'modification', 'suppression'
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    date_action = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.action} - {self.patient} - {self.date_action.strftime('%d/%m/%Y %H:%M')}"

