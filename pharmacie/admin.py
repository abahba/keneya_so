from django.contrib import admin
from django.utils.html import format_html
from .models import CategorieMedicament, Fournisseur, Medicament, HistoriqueMedicament

@admin.register(CategorieMedicament)
class CategorieMedicamentAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)
    ordering = ('nom',)

@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'contact', 'adresse_short')
    search_fields = ('nom', 'contact')
    list_filter = ('nom',)
    
    def adresse_short(self, obj):
        return f"{obj.adresse[:50]}..." if len(obj.adresse) > 50 else obj.adresse
    adresse_short.short_description = 'Adresse'

@admin.register(Medicament)
class MedicamentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'fournisseur', 'stock', 'prix_unitaire', 
                    'date_expiration', 'est_expire', 'actif')
    list_filter = ('categorie', 'fournisseur', 'actif', 'date_expiration')
    search_fields = ('nom', 'description')
    list_editable = ('stock', 'prix_unitaire', 'actif')
    ordering = ('nom',)
    date_hierarchy = 'date_expiration'
    actions = ['marquer_comme_inactif']
    
    fieldsets = (
        (None, {
            'fields': ('nom', 'description', 'categorie', 'fournisseur')
        }),
        ('Stock et Prix', {
            'fields': ('stock', 'prix_unitaire')
        }),
        ('Dates', {
            'fields': ('date_expiration',)
        }),
        ('Statut', {
            'fields': ('actif',)
        }),
    )
    
    def est_expire(self, obj):
        from django.utils import timezone
        if obj.date_expiration < timezone.now().date():
            return format_html('<span style="color: red;">EXPIRÉ</span>')
        return format_html('<span style="color: green;">Valide</span>')
    est_expire.short_description = 'État'
    
    def marquer_comme_inactif(self, request, queryset):
        queryset.update(actif=False)
    marquer_comme_inactif.short_description = "Marquer les médicaments sélectionnés comme inactifs"

@admin.register(HistoriqueMedicament)
class HistoriqueMedicamentAdmin(admin.ModelAdmin):
    list_display = ('medicament', 'action', 'utilisateur', 'date_action', 'details_short')
    list_filter = ('action', 'date_action')
    search_fields = ('medicament__nom', 'utilisateur__username', 'action')
    date_hierarchy = 'date_action'
    readonly_fields = ('medicament', 'utilisateur', 'action', 'date_action', 'details')
    
    def details_short(self, obj):
        return f"{obj.details[:50]}..." if len(obj.details) > 50 else obj.details
    details_short.short_description = 'Détails'

