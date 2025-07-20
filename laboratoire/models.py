from django.db import models

# Create your models here.
from django.db import models
from patients.models import Patient
# Supprimer l'import du modèle Consultation
# et utiliser une référence "app.Model" dans ForeignKey
from django.contrib.auth import get_user_model
User = get_user_model()
from accounts.models import CustomUser
from django.utils import timezone

class TypeAnalyse(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


# laboratoire/models.py
class AnalyseBiologique(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    type_analyse = models.ForeignKey('laboratoire.TypeAnalyse', on_delete=models.CASCADE)
    autre_type_analyse = models.CharField(max_length=255, blank=True, null=True)  # ← il faut ceci si tu veux l'utiliser
    consultation = models.ForeignKey('consultations.Consultation', on_delete=models.SET_NULL, null=True, blank=True)
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    prescripteur = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='analyses_prescrites')
    date_prescription = models.DateTimeField(default=timezone.now)
    
    date_demande = models.DateTimeField(
        default=timezone.now,  # Valeur par défaut = date/heure actuelle
        verbose_name="Date de demande"
    )
    
    def get_resultats(self):
        return self.resultats.all()  # Utilise le related_name='resultats'

class ResultatAnalyse(models.Model):
    analyse = models.ForeignKey(
        'laboratoire.AnalyseBiologique',
        on_delete=models.CASCADE,
        related_name='resultats',  # ← éviter le conflit
    )
    contenu = models.TextField()
    date_resultat = models.DateField(auto_now_add=True)

class HistoriqueAnalyse(models.Model):
    ACTIONS = (
        ('ajout', 'Ajout'),
        ('modification', 'Modification'),
        ('suppression', 'Suppression'),
    )

    analyse = models.ForeignKey(AnalyseBiologique, on_delete=models.CASCADE, related_name='historiques')
    action = models.CharField(max_length=20, choices=ACTIONS)
    utilisateur = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_action_display()} de l'analyse {self.analyse} le {self.date.strftime('%d/%m/%Y %H:%M')}"
