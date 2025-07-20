from django.urls import path
from . import views

app_name = 'urgences'

urlpatterns = [
    path('', views.liste_urgences, name='liste_urgences'),
    path('ajouter/', views.ajouter_urgence, name='ajouter_urgence'),
    path('modifier/<int:urgence_id>/', views.modifier_urgence, name='modifier_urgence'),
    path('supprimer/<int:urgence_id>/', views.supprimer_urgence, name='supprimer_urgence'),
    path('historique/<int:urgence_id>/', views.historique_urgence, name='historique_urgence'),

    # Exports
    path('export/pdf/', views.export_urgences_pdf, name='export_urgences_pdf'),
    path('export/excel/', views.export_urgences_excel, name='export_urgences_excel'),
    path('export/historique/<int:urgence_id>/pdf/', views.export_historique_urgence_pdf, name='export_historique_urgence_pdf'),
    path('export/historique/<int:urgence_id>/excel/', views.export_historique_urgence_excel, name='export_historique_urgence_excel'),
    path('factures/', views.factures_urgences, name='factures_urgences'),

]
