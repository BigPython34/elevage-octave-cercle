from django.contrib import admin
from .models import Elevage

class ElevageAdmin(admin.ModelAdmin):
    list_display = ('nom', 'nombre_lapins_males', 'nombre_lapins_femelles', 'nourriture', 'argent', 'cages', 'total_lapins')
    search_fields = ['nom']

admin.site.register(Elevage, ElevageAdmin)
