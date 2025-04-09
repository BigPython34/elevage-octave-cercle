from django.contrib import admin
from .models import Elevage,Individu

class ElevageAdmin(admin.ModelAdmin):
    list_display = ('nom', 'nombre_lapins_males', 'nombre_lapins_femelles', 'nourriture', 'argent', 'cages', 'total_lapins')
    search_fields = ['nom']

class IndividuAdmin(admin.ModelAdmin):
    list_display = ('sexe', 'age', 'etat', 'elevage')  
    
admin.site.register(Elevage, ElevageAdmin)
admin.site.register(Individu, IndividuAdmin)
