from django.db import models
from patients.models import Patient
from django.contrib.auth import get_user_model

User = get_user_model()

class Soin(models.Model):
    TYPE_SOIN_CHOICES = [
        ('injection', 'Injection'),
        ('perfusion', 'Perfusion'),
        ('pansement', 'Pansement'),
        ('autre', 'Autre'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    type_soin = models.CharField(max_length=20, choices=TYPE_SOIN_CHOICES)
    description = models.TextField(blank=True)
    date_soin = models.DateTimeField(auto_now_add=True)
    personnel = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='soins_realises'
)

    utilisateur = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='soins_enregistres'
)


    def __str__(self):
        return f"{self.get_type_soin_display()} pour {self.patient}"

class HistoriqueSoin(models.Model):
    ACTIONS = [
        ('ajout', 'Ajout'),
        ('modification', 'Modification'),
        ('suppression', 'Suppression'),
    ]

    soin = models.ForeignKey(Soin, on_delete=models.CASCADE, related_name='historiques')
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTIONS)
    details = models.TextField()
    date_action = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_action_display()} - {self.soin}"
