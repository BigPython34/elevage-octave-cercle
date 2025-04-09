from django.contrib import admin
from .models import Elevage

class ElevageAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_lapins_males', 'nombre_lapins_femelles', 'nourriture', 'argent', 'cages', 'total_lapins')
    search_fields = ['nombre_lapins_males', 'nombre_lapins_femelles', 'nourriture', 'argent', 'cages']
    list_filter = ('cages',)

admin.site.register(Elevage, ElevageAdmin)
