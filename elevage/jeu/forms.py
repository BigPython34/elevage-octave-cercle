
from django import forms

class InitialisationForm(forms.Form):
    nom=forms.CharField(label="Nom de l'élevage")
    nb_lapins_males = forms.IntegerField(label='Nombre de mâles', min_value=0)
    nb_lapins_femelles = forms.IntegerField(label='Nombre de femelles', min_value=0)
    nourriture = forms.IntegerField(label='Quantité de nourriture', min_value=0)
    nb_cages = forms.IntegerField(label='Nombre de cages', min_value=0)
    argent = forms.IntegerField(label='Argent ', min_value=0, )

class TourActionForm(forms.Form):
    vendre_males = forms.IntegerField(min_value=0, required=False, label="Lapins mâles à vendre")
    vendre_femelles = forms.IntegerField(min_value=0, required=False, label="Lapins femelles à vendre")
    acheter_nourriture = forms.IntegerField(min_value=0, required=False, label="Quantité de nourriture à acheter (en g)")
    acheter_cages = forms.IntegerField(min_value=0, required=False, label="Nombre de cages à acheter")

    def clean(self):
        cleaned_data = super().clean()
        for field in ['vendre_males', 'vendre_femelles', 'acheter_nourriture', 'acheter_cages']:
            if cleaned_data.get(field) is None:
                cleaned_data[field] = 0
        return cleaned_data
