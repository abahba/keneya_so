from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

from django.contrib import admin
from .models import RendezVous

@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'patient', 'medecin', 'statut']
    list_filter = ['statut', 'date']
    search_fields = ['patient__username', 'medecin__username', 'motif']
    autocomplete_fields = ['patient', 'medecin']
