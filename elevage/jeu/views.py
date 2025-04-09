from django.shortcuts import render, redirect
from .forms import InitialisationForm

def confirmation(request):

    return render(request, 'jeu/confirmation.html')  

def nouveau(request):
    if request.method == 'POST':
        form = InitialisationForm(request.POST)
        if form.is_valid():
            nb_lapins_males = form.cleaned_data['nb_lapins_males']
            nb_lapins_femelles = form.cleaned_data['nb_lapins_femelles']
            nb_lapins_reproducteurs = form.cleaned_data['nb_lapins_reproducteurs']
            nourriture = form.cleaned_data['nourriture']
            nb_cages = form.cleaned_data['nb_cages']
            argent = form.cleaned_data['argent']

            request.session['nb_lapins_males'] = nb_lapins_males
            request.session['nb_lapins_femelles'] = nb_lapins_femelles
            request.session['nb_lapins_reproducteurs'] = nb_lapins_reproducteurs
            request.session['nourriture'] = nourriture
            request.session['nb_cages'] = nb_cages
            request.session['argent'] = argent

            return redirect('jeu:confirmation')  
    else:
        form = InitialisationForm()

    return render(request, 'jeu/nouveau.html', {'form': form})