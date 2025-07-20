from django.contrib import admin
from .models import PersonnelMedical

@admin.register(PersonnelMedical)
class PersonnelMedicalAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'role', 'specialite', 'date_embauche', 'actif')
    list_filter = ('role', 'actif')
    search_fields = ('nom_complet', 'specialite')
    ordering = ('nom_complet',)
    
    # If you want to display the human-readable choice value instead of the DB value
    def get_role_display(self, obj):
        return obj.get_role_display()
    get_role_display.short_description = 'Rôle'
    
    # Add this if you want the choice display in list_display
    list_display = ('nom_complet', 'get_role_display', 'specialite', 'date_embauche', 'actif')

