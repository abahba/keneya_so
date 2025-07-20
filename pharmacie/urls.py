from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_medicaments, name='liste_medicaments'),
    path('ajouter/', views.ajouter_medicament, name='ajouter_medicament'),
    path('<int:pk>/modifier/', views.modifier_medicament, name='modifier_medicament'),
    path('<int:pk>/supprimer/', views.supprimer_medicament, name='supprimer_medicament'),
    path('historique/<int:medicament_id>/pdf/', views.export_historique_medicament_pdf, name='export_historique_medicament_pdf'),
    path('historique/<int:medicament_id>/excel/', views.export_historique_medicament_excel, name='export_historique_medicament_excel'),

]
