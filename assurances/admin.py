from django.contrib import admin
from .models import Assurance, PatientAssure, PriseEnCharge, HistoriqueAssurance

@admin.register(Assurance)
class AssuranceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type', 'couverture')
    search_fields = ('nom',)
    list_filter = ('type',)

@admin.register(PatientAssure)
class PatientAssureAdmin(admin.ModelAdmin):
    list_display = ('patient', 'assurance', 'numero_carte', 'date_expiration', 'actif')
    list_filter = ('actif', 'assurance')
    search_fields = ('patient__nom', 'assurance__nom', 'numero_carte')

@admin.register(PriseEnCharge)
class PriseEnChargeAdmin(admin.ModelAdmin):
    list_display = ('patient', 'assurance', 'date_demande', 'montant_demande', 'montant_approuve', 'statut')
    list_filter = ('statut', 'assurance')
    search_fields = ('patient__nom', 'assurance__nom')
    readonly_fields = ('date_demande',)

@admin.register(HistoriqueAssurance)
class HistoriqueAssuranceAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'action', 'objet', 'description', 'date')
    list_filter = ('action', 'objet')
    search_fields = ('utilisateur__username', 'objet', 'description')
    readonly_fields = ('date',)
