from django.contrib import admin
from .models import TypeAnalyse, AnalyseBiologique, ResultatAnalyse, HistoriqueAnalyse

@admin.register(TypeAnalyse)
class TypeAnalyseAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)

@admin.register(AnalyseBiologique)
class AnalyseBiologiqueAdmin(admin.ModelAdmin):
    list_display = (
        'patient', 'type_analyse', 'consultation',
        'date_prescription', 'prescripteur', 'utilisateur'
    )
    list_filter = ('type_analyse', 'date_prescription')
    search_fields = ('patient__nom', 'type_analyse__nom')
    date_hierarchy = 'date_prescription'

@admin.register(ResultatAnalyse)
class ResultatAnalyseAdmin(admin.ModelAdmin):
    list_display = ('analyse', 'date_resultat')
    search_fields = ('analyse__patient__nom',)
    date_hierarchy = 'date_resultat'

@admin.register(HistoriqueAnalyse)
class HistoriqueAnalyseAdmin(admin.ModelAdmin):
    list_display = ('analyse', 'action', 'utilisateur', 'date', 'description')
    list_filter = ('action', 'date')
    search_fields = ('analyse__patient__nom', 'description')
    date_hierarchy = 'date'
