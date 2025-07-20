from django.contrib import admin
from .models import OperationChirurgicale, HistoriqueOperation

@admin.register(OperationChirurgicale)
class OperationChirurgicaleAdmin(admin.ModelAdmin):
    list_display = (
        'patient', 'date_operation', 'type_operation',
        'salle', 'chirurgien', 'anesthesiste', 'utilisateur'
    )
    list_filter = ('date_operation', 'chirurgien')
    search_fields = ('patient__nom', 'type_operation', 'salle')
    date_hierarchy = 'date_operation'
    ordering = ['-date_operation']

@admin.register(HistoriqueOperation)
class HistoriqueOperationAdmin(admin.ModelAdmin):
    list_display = (
        'operation', 'action', 'utilisateur',
        'date_action', 'details'
    )
    list_filter = ('action', 'date_action')
    search_fields = ('operation__type_operation', 'utilisateur__username')
    date_hierarchy = 'date_action'
