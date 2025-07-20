from django.contrib import admin
from django.utils.html import format_html
from .models import TypeImagerie, ExamenImagerie, HistoriqueImagerie

@admin.register(TypeImagerie)
class TypeImagerieAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)
    ordering = ('nom',)

@admin.register(ExamenImagerie)
class ExamenImagerieAdmin(admin.ModelAdmin):
    list_display = (
        'patient', 
        'type_imagerie', 
        'date_prescription', 
        'prescripteur',
        'resultat_link',
        'consultation_short'
    )
    list_filter = ('type_imagerie', 'date_prescription', 'prescripteur')
    search_fields = ('patient__nom', 'patient__prenom', 'type_imagerie__nom')
    raw_id_fields = ('patient', 'consultation', 'prescripteur', 'utilisateur')
    date_hierarchy = 'date_prescription'
    
    fieldsets = (
        ('Informations patient', {
            'fields': ('patient', 'consultation')
        }),
        ('Détails examen', {
            'fields': ('type_imagerie', 'description', 'fichier_resultat')
        }),
        ('Personnel', {
            'fields': ('prescripteur', 'utilisateur')
        }),
    )
    
    def resultat_link(self, obj):
        if obj.fichier_resultat:
            return format_html(
                '<a href="{}" target="_blank">Voir résultat</a>',
                obj.fichier_resultat.url
            )
        return "Aucun fichier"
    resultat_link.short_description = 'Résultat'
    
    def consultation_short(self, obj):
        if obj.consultation:
            return f"Consultation du {obj.consultation.date_consultation.strftime('%d/%m/%Y')}"
        return "Pas de consultation"
    consultation_short.short_description = 'Consultation'

@admin.register(HistoriqueImagerie)
class HistoriqueImagerieAdmin(admin.ModelAdmin):
    list_display = (
        'patient', 
        'action_colored', 
        'utilisateur', 
        'date_action', 
        'description_short'
    )
    list_filter = ('action', 'date_action', 'utilisateur')
    search_fields = ('patient__nom', 'patient__prenom', 'utilisateur__username')
    readonly_fields = ('utilisateur', 'patient', 'action', 'date_action', 'description')
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
    
    def description_short(self, obj):
        return f"{obj.description[:50]}..." if obj.description and len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'