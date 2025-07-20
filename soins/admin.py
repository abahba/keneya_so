from django.contrib import admin
from django.utils.html import format_html
from .models import Soin, HistoriqueSoin

@admin.register(Soin)
class SoinAdmin(admin.ModelAdmin):
    list_display = (
        'patient',
        'type_soin_display',
        'date_soin',
        'personnel',
        'description_short'
    )
    list_filter = ('type_soin', 'date_soin', 'personnel')
    search_fields = ('patient__nom', 'patient__prenom', 'description')
    raw_id_fields = ('patient', 'personnel', 'utilisateur')
    date_hierarchy = 'date_soin'
    
    fieldsets = (
        ('Informations patient', {
            'fields': ('patient',)
        }),
        ('Détails du soin', {
            'fields': ('type_soin', 'description')
        }),
        ('Personnel', {
            'fields': ('personnel', 'utilisateur')
        }),
    )
    
    def type_soin_display(self, obj):
        return obj.get_type_soin_display()
    type_soin_display.short_description = 'Type de soin'
    
    def description_short(self, obj):
        return f"{obj.description[:50]}..." if obj.description and len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'

@admin.register(HistoriqueSoin)
class HistoriqueSoinAdmin(admin.ModelAdmin):
    list_display = (
        'soin',
        'action_colored',
        'utilisateur',
        'date_action',
        'details_short'
    )
    list_filter = ('action', 'date_action', 'utilisateur')
    search_fields = ('soin__patient__nom', 'soin__patient__prenom', 'details')
    readonly_fields = ('soin', 'utilisateur', 'action', 'date_action', 'details')
    date_hierarchy = 'date_action'
    
    def action_colored(self, obj):
        colors = {
            'ajout': 'green',
            'modification': 'blue',
            'suppression': 'red'
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.action, 'black'),
            obj.get_action_display()
        )
    action_colored.short_description = 'Action'
    
    def details_short(self, obj):
        return f"{obj.details[:50]}..." if obj.details and len(obj.details) > 50 else obj.details
    details_short.short_description = 'Détails'
