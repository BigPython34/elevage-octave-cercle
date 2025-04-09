from django.shortcuts import render, redirect
from .forms import InitialisationForm
from .models import Elevage
def confirmation(request):

    return render(request, 'jeuconfirmation.html')  

def nouveau(request):
    if request.method == 'POST':
        form = InitialisationForm(request.POST)
        if form.is_valid():
            nb_lapins_males = form.cleaned_data['nb_lapins_males']
            nb_lapins_femelles = form.cleaned_data['nb_lapins_femelles']
            
            nourriture = form.cleaned_data['nourriture']
            nb_cages = form.cleaned_data['nb_cages']
            argent = form.cleaned_data['argent']
            nom=form.cleaned_data['nom']
            elevage = Elevage(
            nom=nom,
            nombre_lapins_males=nb_lapins_males,
            nombre_lapins_femelles=nb_lapins_femelles,
            nourriture=nourriture,
            cages=nb_cages,
            argent=argent
            )

            
            elevage.save()

            return redirect('jeu:confirmation')  
    else:
        form = InitialisationForm()

    return render(request, 'jeu/nouveau.html', {'form': form})

def liste(request):

    elevages = Elevage.objects.all()

    return render(request, 'jeu/liste.html', {'elevages': elevages})