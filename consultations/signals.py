from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import PrescriptionAnalyse, Ordonnance, Hospitalisation
from laboratoire.models import AnalyseBiologique
from facturation.models import Facture
from patients.models import Patient


# ✅ Analyse biologique
@receiver(post_save, sender=PrescriptionAnalyse)
def creer_analyse_et_facture(sender, instance, created, **kwargs):
    if created:
        analyse = AnalyseBiologique.objects.create(
            patient=instance.consultation.patient,
            type_analyse=instance.type_analyse,
            autre_type_analyse=instance.autre_type_analyse if not instance.type_analyse else '',
            consultation=instance.consultation,
            date_prescription=timezone.now(),
            prescripteur=instance.prescripteur,
            utilisateur=instance.prescripteur
        )

        montant = analyse.type_analyse.prix if analyse.type_analyse else 5000

        Facture.objects.create(
            patient=analyse.patient,
            montant_total=montant,
            montant_patient=montant,
            utilisateur=analyse.utilisateur,
        )

# ✅ Ordonnance médicale
@receiver(post_save, sender=Ordonnance)
def creer_facture_ordonnance(sender, instance, created, **kwargs):
    if created:
        montant = instance.calculer_montant_total() if hasattr(instance, 'calculer_montant_total') else 10000

        Facture.objects.create(
            patient=instance.consultation.patient,
            ordonnance=instance,
            montant_total=montant,
            montant_patient=montant,
            utilisateur=instance.utilisateur
        )

# ✅ Hospitalisation
@receiver(post_save, sender=Hospitalisation)
def creer_facture_hospitalisation(sender, instance, created, **kwargs):
    if created:
        montant = 20000  # ou instance.tarif si tu as un champ tarif

        Facture.objects.create(
            patient=instance.patient,
            montant_total=montant,
            montant_patient=montant,
            utilisateur=instance.utilisateur
        )


