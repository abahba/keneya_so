from django.urls import path
from . import views

urlpatterns = [
    path('ajouter/', views.ajouter_personnel, name='ajouter_personnel'),
    path('liste/', views.liste_personnel, name='liste_personnel'),
    path('modifier/<int:pk>/', views.modifier_personnel, name='modifier_personnel'),
    path('supprimer/<int:pk>/', views.supprimer_personnel, name='supprimer_personnel'),
    path('historique/<int:personnel_id>/', views.historique_personnel, name='historique_personnel'),
]


