from django.db import models
from django.contrib.auth import get_user_model

# Liens externes
from patients.models import Patient
from consultations.models import Ordonnance, Hospitalisation
from laboratoire.models import AnalyseBiologique
from imagerie.models import ExamenImagerie
from soins.models import Soin
from bloc_operatoire.models import OperationChirurgicale
from assurances.models import Assurance
from urgences.models import Urgence

User = get_user_model()

class Facture(models.Model):
    STATUT_CHOICES = (
        ('non payée', 'Non Payée'),
        ('partiellement payée', 'Partiellement Payée'),
        ('payée', 'Payée'),
    )

    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, verbose_name="Patient")

    # Modules liés (optionnels)
    ordonnance = models.OneToOneField(Ordonnance, on_delete=models.SET_NULL, null=True, blank=True)
    hospitalisation = models.OneToOneField(Hospitalisation, on_delete=models.SET_NULL, null=True, blank=True)
    analyse = models.OneToOneField(AnalyseBiologique, on_delete=models.SET_NULL, null=True, blank=True)
    imagerie = models.OneToOneField(ExamenImagerie, on_delete=models.SET_NULL, null=True, blank=True)
    soin = models.OneToOneField(Soin, on_delete=models.SET_NULL, null=True, blank=True)
    operation = models.OneToOneField(OperationChirurgicale, on_delete=models.SET_NULL, null=True, blank=True)
    urgence = models.OneToOneField(Urgence, on_delete=models.SET_NULL, null=True, blank=True)
    assurance = models.ForeignKey(Assurance, on_delete=models.SET_NULL, null=True, blank=True)

    montant_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant total")
    montant_assurance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    montant_patient = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    date_emission = models.DateTimeField(auto_now_add=True)
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='non payée')

    def __str__(self):
        return f"Facture #{self.id} - {self.patient.nom_complet()}"

    def calculer_statut(self):
        total_payé = sum(p.montant_verse for p in self.paiements.all())
        total_remboursé = sum(r.montant for p in self.paiements.all() for r in p.remboursements.all())
        net = total_payé - total_remboursé

        if net >= self.montant_total:
            self.statut = 'payée'
        elif net > 0:
            self.statut = 'partiellement payée'
        else:
            self.statut = 'non payée'


class Paiement(models.Model):
    MODE_PAIEMENT_CHOICES = [
        ('espèces', 'Espèces'),
        ('orange_money', 'Orange Money'),
        ('moov_money', 'Moov Money'),
        ('wave', 'Wave'),
        ('sama_money', 'Sama Money'),
        ('carte_bancaire', 'Carte Bancaire'),
    ]

    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name='paiements')
    montant_verse = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateTimeField(auto_now_add=True)
    mode_paiement = models.CharField(max_length=50, choices=MODE_PAIEMENT_CHOICES, default='espèces')
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Paiement {self.montant_verse} FCFA pour {self.facture}"


class Remboursement(models.Model):
    paiement = models.ForeignKey(Paiement, on_delete=models.CASCADE, related_name='remboursements')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_remboursement = models.DateTimeField(auto_now_add=True)
    motif = models.CharField(max_length=255)
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Remboursement de {self.montant} FCFA - {self.paiement.facture}"



