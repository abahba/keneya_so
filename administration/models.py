from django.db import models
from personnel.models import PersonnelMedical
from django.db import models
from django.conf import settings

class ServiceHospitalier(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom

class Salle(models.Model):
    service = models.ForeignKey(ServiceHospitalier, on_delete=models.CASCADE, related_name='salles')
    nom = models.CharField(max_length=100)
    type_salle = models.CharField(max_length=100, blank=True, null=True)  # ex : Consultation, Bloc opératoire

    def __str__(self):
        return f"{self.nom} - {self.service.nom}"

class Lit(models.Model):
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE, related_name='lits')
    numero = models.CharField(max_length=10)
    est_occupe = models.BooleanField(default=False)

    def __str__(self):
        return f"Lit {self.numero} ({'Occupé' if self.est_occupe else 'Libre'})"

class Equipement(models.Model):
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE, related_name='equipements')
    nom = models.CharField(max_length=100)
    etat = models.CharField(max_length=50, choices=[
        ('fonctionnel', 'Fonctionnel'),
        ('en panne', 'En panne'),
        ('maintenance', 'Maintenance')
    ], default='fonctionnel')

    def __str__(self):
        return f"{self.nom} - {self.salle.nom}"

class AffectationPersonnel(models.Model):
    personnel = models.ForeignKey(PersonnelMedical, on_delete=models.CASCADE)
    service = models.ForeignKey(ServiceHospitalier, on_delete=models.CASCADE)
    date_affectation = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.personnel.nom_complet()} → {self.service.nom}"

class MembreAdministratif(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nom_complet = models.CharField(max_length=255)
    fonction = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    actif = models.BooleanField(default=True)
    date_embauche = models.DateField()

    def __str__(self):
        return f"{self.nom_complet} - {self.fonction}"

class HistoriqueAdministratif(models.Model):
    membre = models.ForeignKey(MembreAdministratif, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=100)
    date_action = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.action} - {self.membre.nom_complet} - {self.date_action}"
