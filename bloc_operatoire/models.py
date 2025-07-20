from django.db import models
from django.utils import timezone
from patients.models import Patient
from accounts.models import CustomUser
from personnel.models import PersonnelMedical

class OperationChirurgicale(models.Model):
    """Modèle représentant une opération chirurgicale"""
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        verbose_name="Patient"
    )
    date_operation = models.DateTimeField(
        default=timezone.now,
        verbose_name="Date et heure de l'opération"
    )
    type_operation = models.CharField(
        max_length=200,
        verbose_name="Type d'opération"
    )
    salle = models.CharField(
        max_length=100,
        verbose_name="Salle d'opération"
    )
    chirurgien = models.ForeignKey(
        PersonnelMedical,
        on_delete=models.SET_NULL,
        null=True,
        related_name='operations_chirurgien',
        verbose_name="Chirurgien principal"
    )
    anesthesiste = models.ForeignKey(
        PersonnelMedical,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='operations_anesthesiste',
        verbose_name="Anesthésiste"
    )
    compte_rendu = models.TextField(
        blank=True,
        verbose_name="Compte rendu opératoire"
    )
    observations = models.TextField(
        blank=True,
        verbose_name="Observations"
    )
    utilisateur = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Utilisateur"
    )
    date_enregistrement = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'enregistrement"
    )

    class Meta:
        verbose_name = "Opération chirurgicale"
        verbose_name_plural = "Opérations chirurgicales"
        ordering = ['-date_operation']

    def __str__(self):
        return f"{self.patient.nom_complet()} - {self.type_operation} ({self.date_operation.date()})"


class HistoriqueOperation(models.Model):
    """Modèle pour tracer les modifications des opérations"""
    operation = models.ForeignKey(
        OperationChirurgicale,
        on_delete=models.CASCADE,
        related_name='historiques',
        verbose_name="Opération"
    )
    utilisateur = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Utilisateur"
    )
    action = models.CharField(
        max_length=100,
        choices=[
            ('ajout', 'Ajout'),
            ('modification', 'Modification'),
            ('suppression', 'Suppression')
        ],
        verbose_name="Action effectuée"
    )
    date_action = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de l'action"
    )
    details = models.TextField(
        blank=True,
        verbose_name="Détails supplémentaires"
    )

    class Meta:
        verbose_name = "Historique d'opération"
        verbose_name_plural = "Historiques d'opérations"
        ordering = ['-date_action']

    def __str__(self):
        return f"{self.operation} - {self.get_action_display()} - {self.date_action.strftime('%d/%m/%Y %H:%M')}"
    