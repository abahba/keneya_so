from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_examens_imagerie, name='liste_examens_imagerie'),
    path('ajouter/', views.ajouter_examen_imagerie, name='ajouter_examen_imagerie'),
    path('modifier/<int:examen_id>/', views.modifier_examen_imagerie, name='modifier_examen_imagerie'),
    path('supprimer/<int:examen_id>/', views.supprimer_examen_imagerie, name='supprimer_examen_imagerie'),
    path('examen/<int:examen_id>/historique/', views.historique_examen_imagerie, name='historique_examen_imagerie'),
    path('examen/<int:examen_id>/export_pdf/', views.export_historique_imagerie_pdf, name='export_historique_imagerie_pdf'),
    path('examen/<int:examen_id>/export_excel/', views.export_historique_imagerie_excel, name='export_historique_imagerie_excel'),
]
