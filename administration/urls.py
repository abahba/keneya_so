from django.urls import path
from . import views

app_name = 'administration'

urlpatterns = [
    path('', views.liste_membres, name='liste_membres'),
    path('ajouter/', views.ajouter_membre, name='ajouter_membre'),
    path('modifier/<int:pk>/', views.modifier_membre, name='modifier_membre'),
    path('supprimer/<int:pk>/', views.supprimer_membre, name='supprimer_membre'),

    # Historique
    path('historique/', views.historique_membres, name='historique_membres'),

    # Export PDF / Excel
    path('export/pdf/', views.export_membres_pdf, name='export_membres_pdf'),
    path('export/excel/', views.export_membres_excel, name='export_membres_excel'),
]

