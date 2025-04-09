from django.urls import path
from . import views


app_name = 'jeu'

urlpatterns = [
    path('nouveau/', views.nouveau, name='nouveau'),  
    path('confirmation/', views.confirmation, name='confirmation'),  
    path('liste/', views.liste, name='liste_elevages')
]