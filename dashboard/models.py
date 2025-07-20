from django.db import models

class ParametresSysteme(models.Model):
    nom_hopital = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    fuseau_horaire = models.CharField(max_length=100, default='Africa/Bamako')
    contact = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    adresse = models.TextField(blank=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom_hopital
