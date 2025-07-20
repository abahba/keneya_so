from django.contrib import admin
from .models import ParametresSysteme

@admin.register(ParametresSysteme)
class ParametresSystemeAdmin(admin.ModelAdmin):
    list_display = ['nom_hopital', 'fuseau_horaire', 'contact', 'email', 'date_modification']
    search_fields = ['nom_hopital', 'contact', 'email', 'adresse']
    list_filter = ['fuseau_horaire', 'date_modification']
