from django.urls import path
from .views import redirection_tableau_de_bord
from . import views
urlpatterns = [
    path('dashboard/', redirection_tableau_de_bord, name='dashboard'),
    path('', views.index, name='index'),  # Page d’accueil
    path('dashboard/', views.redirection_tableau_de_bord, name='dashboard'),  # Redirection selon rôle
]

