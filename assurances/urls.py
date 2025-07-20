from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil_assurances, name='accueil_assurances'),
    path('assurances/', views.liste_assurances, name='liste_assurances'),
    path('assurances/ajouter/', views.ajouter_assurance, name='ajouter_assurance'),

    path('patients-assures/', views.liste_patients_assures, name='liste_patients_assures'),
    path('patients-assures/ajouter/', views.ajouter_patient_assure, name='ajouter_patient_assure'),

    path('prises-en-charge/', views.liste_prises_en_charge, name='liste_prises_en_charge'),
    path('prises-en-charge/ajouter/', views.ajouter_prise_en_charge, name='ajouter_prise_en_charge'),

    path('export/pdf/', views.export_prises_pdf, name='export_prises_pdf'),
    path('export/excel/', views.export_prises_excel, name='export_prises_excel'),
    path('historique/', views.historique_assurances, name='historique_assurances'),

]
