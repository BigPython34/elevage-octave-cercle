
from django import forms

class InitialisationForm(forms.Form):
    nb_lapins_males = forms.IntegerField(label='Nombre de mâles', min_value=0)
    nb_lapins_femelles = forms.IntegerField(label='Nombre de femelles', min_value=0)
    nb_lapins_reproducteurs = forms.IntegerField(label='Nombre de lapins reproducteurs', min_value=0)
    nourriture = forms.IntegerField(label='Quantité de nourriture', min_value=0)
    nb_cages = forms.IntegerField(label='Nombre de cages', min_value=0)
    argent = forms.IntegerField(label='Argent ', min_value=0, )
