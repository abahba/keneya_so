from django.db import models
from django.conf import settings
from django.utils import timezone
from patients.models import Patient
from assurances.models import Assurance, PriseEnCharge
from laboratoire.models import TypeAnalyse
from accounts.models import CustomUser

# Choix de type d'assurance
TYPE_ASSURANCE_CHOICES = [
    ('classique', 'Classique'),
    ('amo', 'Assurance Maladie Obligatoire (AMO)'),
    ('nsia assurances', 'Nsia assurances'),
    ('sabuyuman', 'Sabuyuman'),
    ('autres', 'Autres'),
]

from django.db import models
from django.conf import settings
from django.utils import timezone
from patients.models import Patient
from assurances.models import Assurance, PriseEnCharge
from accounts.models import CustomUser

TYPE_ASSURANCE_CHOICES = [
    ('classique', 'Classique'),
    ('amo', 'Assurance Maladie Obligatoire (AMO)'),
    ('nsia assurances', 'Nsia assurances'),
    ('sabuyuman', 'Sabuyuman'),
    ('autres', 'Autres'),
]

class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations')
    medecin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    date_consultation = models.DateTimeField(auto_now_add=True)
    symptomes = models.TextField()
    diagnostic = models.TextField()
    traitement = models.TextField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Consultation de {self.patient.nom} {self.patient.prenom} le {self.date_consultation.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        ordering = ['-date_consultation']


class HistoriqueConsultation(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='historiques')
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)
    date_action = models.DateTimeField(default=timezone.now)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.action} - {self.consultation} - {self.date_action.strftime('%d/%m/%Y %H:%M')}"


class DossierMedical(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    antecedents = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    traitements_en_cours = models.TextField(blank=True)
    autres_infos = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Dossier de {self.patient.nom} {self.patient.prenom}"


class Ordonnance(models.Model):
    consultation = models.OneToOneField(Consultation, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    type_assurance = models.CharField(max_length=50, choices=TYPE_ASSURANCE_CHOICES, default='classique')
    signature = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    assurance = models.ForeignKey(Assurance, on_delete=models.SET_NULL, null=True, blank=True)
    prise_en_charge = models.OneToOneField(PriseEnCharge, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Ordonnance de {self.consultation.patient}"


class LigneOrdonnance(models.Model):
    ordonnance = models.ForeignKey(Ordonnance, on_delete=models.CASCADE, related_name='lignes')
    medicament = models.ForeignKey('pharmacie.Medicament', on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    posologie = models.TextField()
    duree = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.medicament.nom} x{self.quantite}"


class ServiceHospitalier(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom


class Hospitalisation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='hospitalisations')
    service = models.ForeignKey(ServiceHospitalier, on_delete=models.SET_NULL, null=True)
    date_entree = models.DateTimeField(default=timezone.now)
    date_sortie = models.DateTimeField(null=True, blank=True)
    motif = models.TextField()
    medecin_responsable = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    related_name='hospitalisations_medecin'
)
    utilisateur = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    related_name='hospitalisations_utilisateur'
)

    def __str__(self):
        return f"Hospitalisation de {self.patient} - {self.service} - {self.date_entree.strftime('%d/%m/%Y')}"

class HistoriqueHospitalisation(models.Model):
    hospitalisation = models.ForeignKey(Hospitalisation, on_delete=models.CASCADE, related_name='historiques')
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)
    date_action = models.DateTimeField(default=timezone.now)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.action} - {self.hospitalisation.patient.nom} - {self.date_action.strftime('%d/%m/%Y %H:%M')}"


class PrescriptionAnalyse(models.Model):
    consultation = models.ForeignKey('consultations.Consultation', on_delete=models.CASCADE, related_name='prescriptions_analyse')
    type_analyse = models.ForeignKey('laboratoire.TypeAnalyse', on_delete=models.CASCADE)
    autre_type_analyse = models.CharField(max_length=255, blank=True, null=True)
    date_prescription = models.DateTimeField(auto_now_add=True)
    prescripteur = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.type_analyse.nom} pour {self.consultation.patient.nom_complet}"



