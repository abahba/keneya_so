from django.contrib import admin
from django.utils.html import format_html
from .models import Patient, HistoriquePatient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'numero_dossier_short',
        'nom_complet',
        'age',
        'sexe',
        'statut_colored',
        'telephone',
        'actif'
    )
    list_filter = ('sexe', 'statut', 'actif', 'date_creation')
    search_fields = ('nom', 'prenom', 'numero_dossier', 'telephone')
    list_editable = ('actif',)
    ordering = ('-date_creation',)
    date_hierarchy = 'date_creation'
    
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'prenom', 'date_naissance', 'sexe')
        }),
        ('Coordonnées', {
            'fields': ('adresse', 'telephone')
        }),
        ('Statut hospitalier', {
            'fields': ('statut', 'date_sortie', 'signature_sortie', 'date_deces', 'signature_deces')
        }),
        ('Administratif', {
            'fields': ('actif',)
        }),
    )
    
    def numero_dossier_short(self, obj):
        return str(obj.numero_dossier)[:8]
    numero_dossier_short.short_description = 'N° Dossier'
    
    def nom_complet(self, obj):
        return f"{obj.nom} {obj.prenom}"
    nom_complet.short_description = 'Nom complet'
    
    def age(self, obj):
        from datetime import date
        today = date.today()
        return today.year - obj.date_naissance.year - ((today.month, today.day) < (obj.date_naissance.month, obj.date_naissance.day))
    age.short_description = 'Âge'
    
    def statut_colored(self, obj):
        colors = {
            'consulté': 'blue',
            'hospitalisé': 'orange',
            'sorti': 'green',
            'décédé': 'red'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.statut, 'black'),
            obj.get_statut_display()
        )
    statut_colored.short_description = 'Statut'

@admin.register(HistoriquePatient)
class HistoriquePatientAdmin(admin.ModelAdmin):
    list_display = (
        'patient',
        'action_colored',
        'utilisateur',
        'date_action',
        'details_short'
    )
    list_filter = ('action', 'date_action', 'utilisateur')
    search_fields = ('patient__nom', 'patient__prenom', 'action')
    readonly_fields = ('patient', 'utilisateur', 'action', 'date_action', 'details')
    date_hierarchy = 'date_action'
    
    def action_colored(self, obj):
        colors = {
            'création': 'green',
            'modification': 'blue',
            'suppression': 'red'
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.action.lower(), 'black'),
            obj.action
        )
    action_colored.short_description = 'Action'
    
    def details_short(self, obj):
        return f"{obj.details[:50]}..." if obj.details and len(obj.details) > 50 else obj.details
    details_short.short_description = 'Détails'