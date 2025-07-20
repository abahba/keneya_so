from django.contrib import admin
from .models import Facture, Paiement, Remboursement


@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'montant_total', 'montant_assurance', 'montant_patient', 'statut', 'date_emission')
    list_filter = ('statut', 'date_emission', 'assurance')
    search_fields = ('patient__nom', 'patient__prenom')
    date_hierarchy = 'date_emission'
    autocomplete_fields = ['patient', 'assurance', 'ordonnance', 'hospitalisation', 'analyse', 'imagerie', 'soin', 'operation', 'urgence']
    readonly_fields = ('date_emission',)


@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ('id', 'facture', 'montant_verse', 'mode_paiement', 'date_paiement')
    list_filter = ('mode_paiement', 'date_paiement')
    search_fields = ('facture__id', 'facture__patient__nom', 'facture__patient__prenom')
    date_hierarchy = 'date_paiement'
    autocomplete_fields = ['facture']


@admin.register(Remboursement)
class RemboursementAdmin(admin.ModelAdmin):
    list_display = ('id', 'paiement', 'montant', 'motif', 'date_remboursement')
    list_filter = ('date_remboursement',)
    search_fields = ('paiement__facture__id', 'paiement__facture__patient__nom')
    date_hierarchy = 'date_remboursement'
    autocomplete_fields = ['paiement']
