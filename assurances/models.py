from django.db import models

# Create your models here.
from django.db import models
from patients.models import Patient  # Ajuste si Patient est dans une autre app
from django.contrib.auth import get_user_model

class Assurance(models.Model):
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=[
        ('AMO', 'AMO'),
        ('PRIVEE', 'Privée'),
    ])
    couverture = models.DecimalField(
        max_digits=5, decimal_places=2,
        help_text="Pourcentage de prise en charge (ex: 80%)"
    )

    def __str__(self):
        return self.nom


class PatientAssure(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    assurance = models.ForeignKey(Assurance, on_delete=models.CASCADE)
    numero_carte = models.CharField(max_length=100)
    date_expiration = models.DateField()
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.patient.nom_complet()} - {self.assurance.nom}"


class PriseEnCharge(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    assurance = models.ForeignKey(Assurance, on_delete=models.CASCADE)
    date_demande = models.DateTimeField(auto_now_add=True)
    montant_demande = models.DecimalField(max_digits=10, decimal_places=2)
    montant_approuve = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    statut = models.CharField(max_length=50, choices=[
        ('en_attente', 'En attente'),
        ('approuvee', 'Approuvée'),
        ('rejetee', 'Rejetée'),
    ], default='en_attente')

    def __str__(self):
        return f"{self.patient.nom_complet()} - {self.statut}"

User = get_user_model()

class HistoriqueAssurance(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)  # ajout, modification, suppression
    objet = models.CharField(max_length=100)  # Assurance, PatientAssure, PriseEnCharge
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur} - {self.action} sur {self.objet} à {self.date.strftime('%d/%m/%Y %H:%M')}"
