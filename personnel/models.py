from django.db import models
from django.conf import settings
from django.utils import timezone

class PersonnelMedical(models.Model):
    ROLE_CHOICES = [
        ('medecin', 'Médecin'),
        ('infirmier', 'Infirmier'),
        ('pharmacien', 'Pharmacien'),
        ('laborantin', 'Laborantin'),
        ('imagerie', 'Technicien Imagerie'),
        ('chirurgien', 'Chirurgien'), 
        ('anesthesiste', 'Anesthésiste'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nom_complet = models.CharField(max_length=255)
    specialite = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    date_embauche = models.DateField()
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Personnel médical"
        verbose_name_plural = "Personnel médical"

    def __str__(self):
        return f"{self.nom_complet} - {self.get_role_display()}"

class HistoriquePersonnel(models.Model):
    personnel = models.ForeignKey(
        'personnel.PersonnelMedical',  # Référence explicite
        on_delete=models.CASCADE,
        related_name='historiques'
    )
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    date_action = models.DateTimeField(default=timezone.now)
    details = models.TextField(blank=True)

    class Meta:
        verbose_name = "Historique personnel"
        verbose_name_plural = "Historiques personnel"

    def __str__(self):
        return f"{self.action} - {self.personnel} - {self.date_action}"