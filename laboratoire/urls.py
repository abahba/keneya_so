from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_analyses, name='liste_analyses'),
    path('ajouter/', views.ajouter_analyse, name='ajouter_analyse'),
    path('modifier/<int:analyse_id>/', views.modifier_analyse, name='modifier_analyse'),
    path('ajouter-resultat/<int:analyse_id>/', views.ajouter_resultat, name='ajouter_resultat'),
    path('detail/<int:analyse_id>/', views.detail_analyse, name='detail_analyse'),
    path('historique/<int:analyse_id>/', views.historique_analyse, name='historique_analyse'),
    path('export-pdf/', views.export_analyses_pdf, name='export_analyses_pdf'),
    path('export-excel/', views.export_analyses_excel, name='export_analyses_excel'),
    path('factures/analyses/', views.factures_analyses, name='factures_analyses'),
]

