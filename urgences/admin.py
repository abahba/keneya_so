from django.contrib import admin
from django.utils.html import format_html
from .models import PassageUrgence, HistoriqueUrgence, Urgence

@admin.register(PassageUrgence)
class PassageUrgenceAdmin(admin.ModelAdmin):
    list_display = (
        'patient',
        'date_arrivee',
        'gravite_colored',
        'motif_short',
        'medecin_responsable',
        'oriente_vers'
    )
    list_filter = ('gravite', 'date_arrivee', 'medecin_responsable')
    search_fields = ('patient__nom_complet', 'motif', 'prise_en_charge')
    raw_id_fields = ('patient', 'medecin_responsable', 'utilisateur')
    date_hierarchy = 'date_arrivee'
    ordering = ('-date_arrivee',)
    
    fieldsets = (
        ('Informations patient', {
            'fields': ('patient', 'date_arrivee')
        }),
        ('Détails urgence', {
            'fields': ('motif', 'gravite', 'prise_en_charge', 'oriente_vers')
        }),
        ('Personnel', {
            'fields': ('medecin_responsable', 'utilisateur')
        }),
    )
    
    def gravite_colored(self, obj):
        colors = {
            'faible': 'green',
            'moyenne': 'orange',
            'grave': 'red',
            'critique': 'purple'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.gravite, 'black'),
            obj.get_gravite_display()
        )
    gravite_colored.short_description = 'Gravité'
    
    def motif_short(self, obj):
        return f"{obj.motif[:50]}..." if len(obj.motif) > 50 else obj.motif
    motif_short.short_description = 'Motif'

@admin.register(HistoriqueUrgence)
class HistoriqueUrgenceAdmin(admin.ModelAdmin):
    list_display = (
        'passage',
        'action_colored',
        'utilisateur',
        'date_action',
        'details_short'
    )
    list_filter = ('action', 'date_action', 'utilisateur')
    search_fields = ('passage__patient__nom_complet', 'action', 'details')
    readonly_fields = ('passage', 'utilisateur', 'action', 'date_action', 'details')
    date_hierarchy = 'date_action'
    
    def action_colored(self, obj):
        colors = {
            'ajout': 'green',
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

@admin.register(Urgence)
class UrgenceAdmin(admin.ModelAdmin):
    list_display = (
        'patient',
        'date_arrivee',
        'motif_short'
    )
    list_filter = ('date_arrivee',)
    search_fields = ('patient__nom_complet', 'motif')
    raw_id_fields = ('patient',)
    date_hierarchy = 'date_arrivee'
    
    def motif_short(self, obj):
        return f"{obj.motif[:50]}..." if len(obj.motif) > 50 else obj.motif
    motif_short.short_description = 'Motif'