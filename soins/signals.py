from django.db.models.signals import post_save
from django.dispatch import receiver
from facturation.models import Facture
from .models import Soin
@receiver(post_save, sender=Soin)
def creer_facture_soin(sender, instance, created, **kwargs):
    if created:
        Facture.objects.create(
            patient=instance.patient,
            montant_total=instance.tarif,
            montant_patient=instance.tarif,
            utilisateur=instance.utilisateur
        )