from django.urls import path
from .views import ajouter_patient
from .views import liste_patients
from . import views
urlpatterns = [
    path('ajouter/', ajouter_patient, name='ajouter_patient'),
    path('liste/', liste_patients, name='liste_patients'),
    path('modifier/<int:pk>/', views.modifier_patient, name='modifier_patient'),
    path('supprimer/<int:pk>/', views.supprimer_patient, name='supprimer_patient'),
    path('', views.liste_patients, name='liste_patients'),
    path('ajouter/', views.ajouter_patient, name='ajouter_patient'),
    path('<int:patient_id>/modifier/', views.modifier_patient, name='modifier_patient'),
    path('<int:pk>/supprimer/', views.supprimer_patient, name='supprimer_patient'),
    path('<int:patient_id>/historique/', views.historique_patient, name='historique_patient'),
    path('<int:patient_id>/historique/pdf/', views.export_pdf_historique, name='export_pdf_historique'),
    path('<int:patient_id>/historique/excel/', views.export_excel_historique, name='export_excel_historique'),
]
