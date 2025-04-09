from django.urls import path
from . import views


app_name = 'jeu'

urlpatterns = [
    path('nouveau/', views.nouveau, name='nouveau'),  # Vue pour la page de création de la partie
    path('confirmation/', views.confirmation, name='confirmation'),  # Exemple de vue pour confirmation
]