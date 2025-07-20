from django.db import models
from django.utils import timezone
from django.conf import settings

class CategorieMedicament(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom


class Fournisseur(models.Model):
    nom = models.CharField(max_length=255)
    contact = models.CharField(max_length=100, blank=True)
    adresse = models.TextField(blank=True)

    def __str__(self):
        return self.nom


class Medicament(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    categorie = models.ForeignKey(CategorieMedicament, on_delete=models.SET_NULL, null=True, blank=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    date_expiration = models.DateField()
    actif = models.BooleanField(default=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

class HistoriqueMedicament(models.Model):
    medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE, related_name='historiques')
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)  # ajout, modification, suppression
    date_action = models.DateTimeField(default=timezone.now)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.action} - {self.medicament.nom} - {self.date_action.strftime('%d/%m/%Y %H:%M')}"

