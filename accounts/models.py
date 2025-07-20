from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('medecin', 'Médecin'),
        ('infirmier', 'Infirmier'),
        ('pharmacien', 'Pharmacien'),
        ('laborantin', 'Laborantin'),
        ('imagerie', 'Imagerie'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='infirmier')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class RendezVous(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rendezvous_patient')
    medecin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rendezvous_medecin')
    date = models.DateTimeField()
    motif = models.TextField()
    notes = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=20, choices=[
        ('planifie', 'Planifié'),
        ('annule', 'Annulé'),
        ('termine', 'Terminé'),
    ], default='planifie')

    class Meta:
        verbose_name = "Rendez-vous"
        verbose_name_plural = "Rendez-vous"
        ordering = ['date']

    def __str__(self):
        return f"Rendez-vous du {self.date} - {self.patient} avec {self.medecin}"