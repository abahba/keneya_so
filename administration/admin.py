from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ServiceHospitalier, Salle, Lit, Equipement,
    AffectationPersonnel, MembreAdministratif, HistoriqueAdministratif
)

@admin.register(ServiceHospitalier)
class ServiceHospitalierAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description_short')
    search_fields = ('nom',)
    ordering = ('nom',)
    
    def description_short(self, obj):
        return f"{obj.description[:50]}..." if obj.description and len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'

@admin.register(Salle)
class SalleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'service', 'type_salle', 'nb_lits', 'nb_lits_occupes')
    list_filter = ('service', 'type_salle')
    search_fields = ('nom', 'service__nom')
    raw_id_fields = ('service',)
    
    def nb_lits(self, obj):
        return obj.lits.count()
    nb_lits.short_description = 'Total lits'
    
    def nb_lits_occupes(self, obj):
        return obj.lits.filter(est_occupe=True).count()
    nb_lits_occupes.short_description = 'Lits occupés'

@admin.register(Lit)
class LitAdmin(admin.ModelAdmin):
    list_display = ('numero', 'salle', 'service', 'est_occupe', 'est_occupe_colored')  # Added 'est_occupe' to list_display
    list_filter = ('salle__service', 'est_occupe')
    search_fields = ('numero', 'salle__nom')
    list_editable = ('est_occupe',)  # Now 'est_occupe' is in list_display
    raw_id_fields = ('salle',)
    
    def service(self, obj):
        return obj.salle.service
    service.short_description = 'Service'
    
    def est_occupe_colored(self, obj):
        if obj.est_occupe:
            return format_html('<span style="color: red;">Occupé</span>')
        return format_html('<span style="color: green;">Libre</span>')
    est_occupe_colored.short_description = 'Statut (colored)'

@admin.register(Equipement)
class EquipementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'salle', 'service', 'etat', 'etat_colored')  # Added 'etat' to list_display
    list_filter = ('etat', 'salle__service')
    search_fields = ('nom', 'salle__nom')
    list_editable = ('etat',)  # Now 'etat' is in list_display
    raw_id_fields = ('salle',)
    
    def service(self, obj):
        return obj.salle.service
    service.short_description = 'Service'
    
    def etat_colored(self, obj):
        if obj.etat == 'fonctionnel':
            return format_html('<span style="color: green;">Fonctionnel</span>')
        elif obj.etat == 'en panne':
            return format_html('<span style="color: red;">En panne</span>')
        return format_html('<span style="color: orange;">Maintenance</span>')
    etat_colored.short_description = 'État (colored)'

@admin.register(AffectationPersonnel)
class AffectationPersonnelAdmin(admin.ModelAdmin):
    list_display = ('personnel', 'service', 'date_affectation')
    list_filter = ('service', 'date_affectation')
    search_fields = ('personnel__nom_complet', 'service__nom')
    raw_id_fields = ('personnel', 'service')
    date_hierarchy = 'date_affectation'

@admin.register(MembreAdministratif)
class MembreAdministratifAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'fonction', 'telephone', 'actif', 'date_embauche')
    list_filter = ('fonction', 'actif')
    search_fields = ('nom_complet', 'telephone')
    list_editable = ('actif',)
    raw_id_fields = ('user',)
    
    fieldsets = (
        ('Identité', {
            'fields': ('user', 'nom_complet', 'telephone')
        }),
        ('Fonction', {
            'fields': ('fonction', 'date_embauche', 'actif')
        }),
    )

@admin.register(HistoriqueAdministratif)
class HistoriqueAdministratifAdmin(admin.ModelAdmin):
    list_display = ('membre', 'action', 'utilisateur', 'date_action', 'details_short')
    list_filter = ('action', 'date_action')
    search_fields = ('membre__nom_complet', 'action')
    readonly_fields = ('membre', 'utilisateur', 'action', 'date_action', 'details')
    date_hierarchy = 'date_action'
    
    def details_short(self, obj):
        return f"{obj.details[:50]}..." if obj.details and len(obj.details) > 50 else obj.details
    details_short.short_description = 'Détails'