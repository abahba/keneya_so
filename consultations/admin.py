from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Consultation, HistoriqueConsultation, DossierMedical,
    Ordonnance, LigneOrdonnance, ServiceHospitalier,
    Hospitalisation, HistoriqueHospitalisation, PrescriptionAnalyse
)

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'medecin', 'date_consultation', 'symptomes_short', 'diagnostic_short')
    list_filter = ('medecin', 'date_consultation')
    search_fields = ('patient__nom', 'patient__prenom', 'medecin__username', 'diagnostic')
    date_hierarchy = 'date_consultation'
    ordering = ('-date_consultation',)
    raw_id_fields = ('patient', 'medecin')
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('patient', 'medecin')
        }),
        ('Détails cliniques', {
            'fields': ('symptomes', 'diagnostic', 'traitement', 'notes')
        }),
    )
    
    def symptomes_short(self, obj):
        return f"{obj.symptomes[:50]}..." if len(obj.symptomes) > 50 else obj.symptomes
    symptomes_short.short_description = 'Symptômes'
    
    def diagnostic_short(self, obj):
        return f"{obj.diagnostic[:50]}..." if len(obj.diagnostic) > 50 else obj.diagnostic
    diagnostic_short.short_description = 'Diagnostic'

@admin.register(HistoriqueConsultation)
class HistoriqueConsultationAdmin(admin.ModelAdmin):
    list_display = ('consultation', 'action', 'utilisateur', 'date_action', 'details_short')
    list_filter = ('action', 'date_action', 'utilisateur')
    search_fields = ('consultation__patient__nom', 'action')
    date_hierarchy = 'date_action'
    readonly_fields = ('consultation', 'utilisateur', 'action', 'date_action', 'details')
    
    def details_short(self, obj):
        return f"{obj.details[:50]}..." if len(obj.details) > 50 else obj.details
    details_short.short_description = 'Détails'

@admin.register(DossierMedical)
class DossierMedicalAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date_creation', 'auteur')
    search_fields = ('patient__nom', 'patient__prenom')
    raw_id_fields = ('patient', 'auteur')
    
    fieldsets = (
        ('Informations patient', {
            'fields': ('patient',)
        }),
        ('Antécédents médicaux', {
            'fields': ('antecedents', 'allergies', 'traitements_en_cours')
        }),
        ('Autres informations', {
            'fields': ('autres_infos',)
        }),
    )

@admin.register(Ordonnance)
class OrdonnanceAdmin(admin.ModelAdmin):
    list_display = ('consultation', 'type_assurance', 'assurance', 'date_creation', 'signature')
    list_filter = ('type_assurance', 'assurance', 'date_creation')
    search_fields = ('consultation__patient__nom',)
    raw_id_fields = ('consultation', 'signature', 'assurance', 'prise_en_charge')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'consultation__patient',
            'assurance',
            'signature'
        )

@admin.register(LigneOrdonnance)
class LigneOrdonnanceAdmin(admin.ModelAdmin):
    list_display = ('ordonnance', 'medicament', 'quantite', 'posologie_short', 'duree')
    list_filter = ('medicament',)
    search_fields = ('ordonnance__consultation__patient__nom', 'medicament__nom')
    raw_id_fields = ('ordonnance', 'medicament')
    
    def posologie_short(self, obj):
        return f"{obj.posologie[:30]}..." if len(obj.posologie) > 30 else obj.posologie
    posologie_short.short_description = 'Posologie'

@admin.register(ServiceHospitalier)
class ServiceHospitalierAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)

@admin.register(Hospitalisation)
class HospitalisationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'service', 'date_entree', 'date_sortie', 'statut')
    list_filter = ('service', 'date_entree', 'medecin_responsable')
    search_fields = ('patient__nom', 'patient__prenom')
    raw_id_fields = ('patient', 'service', 'medecin_responsable', 'utilisateur')
    date_hierarchy = 'date_entree'
    
    def statut(self, obj):
        if obj.date_sortie:
            return format_html('<span style="color: green;">Sorti</span>')
        return format_html('<span style="color: red;">Hospitalisé</span>')
    statut.short_description = 'Statut'

@admin.register(HistoriqueHospitalisation)
class HistoriqueHospitalisationAdmin(admin.ModelAdmin):
    list_display = ('hospitalisation', 'action', 'utilisateur', 'date_action')
    list_filter = ('action', 'date_action')
    search_fields = ('hospitalisation__patient__nom',)
    date_hierarchy = 'date_action'
    readonly_fields = ('hospitalisation', 'utilisateur', 'action', 'date_action', 'details')

@admin.register(PrescriptionAnalyse)
class PrescriptionAnalyseAdmin(admin.ModelAdmin):
    list_display = ('consultation', 'type_analyse', 'date_prescription', 'prescripteur')
    list_filter = ('type_analyse', 'date_prescription')
    search_fields = ('consultation__patient__nom', 'type_analyse__nom')
    raw_id_fields = ('consultation', 'type_analyse', 'prescripteur')
