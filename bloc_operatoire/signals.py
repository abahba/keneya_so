from django.db.models.signals import post_save
from django.dispatch import receiver
from facturation.models import Facture
from .models import BlocOperatoire

@receiver(post_save, sender=BlocOperatoire)
def creer_facture_bloc_operatoire(sender, instance, created, **kwargs):
    if created:
        Facture.objects.create(
            patient=instance.patient,
            montant_total=instance.tarif,
            montant_patient=instance.tarif,
            utilisateur=instance.utilisateur
        )
