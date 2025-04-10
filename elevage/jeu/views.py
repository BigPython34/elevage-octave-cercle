from django.shortcuts import render, redirect,get_object_or_404
from .forms import InitialisationForm,TourActionForm
from .models import Elevage,Individu,Regle
from django.contrib import messages
def confirmation(request):

    return render(request, 'jeu:confirmation.html')  

def nouveau(request):
    if request.method == 'POST':
        form = InitialisationForm(request.POST)
        if form.is_valid():

            nom = form.cleaned_data['nom']
            nb_lapins_males = form.cleaned_data['nb_lapins_males']
            nb_lapins_femelles = form.cleaned_data['nb_lapins_femelles']
            nourriture = form.cleaned_data['nourriture']
            nb_cages = form.cleaned_data['nb_cages']
            argent = form.cleaned_data['argent']
            if Elevage.objects.filter(nom=nom).exists():
                messages.error(request, "Un élevage avec ce nom existe déjà.")
                return redirect('jeu:nouveau')  # Rediriger vers le formulaire pour corriger

            elevage = Elevage(
                nom=nom,
                nourriture=nourriture,
                cages=nb_cages,
                argent=argent
            )


            regle = Regle.objects.first()  
            if regle:
                elevage.regle = regle


            elevage.save()


            for _ in range(nb_lapins_males):
                Individu.objects.create(sexe='m', age=0, etat='present', elevage=elevage)
            for _ in range(nb_lapins_femelles):
                Individu.objects.create(sexe='f', age=0, etat='present', elevage=elevage)


            return redirect('jeu:confirmation')
    else:
        form = InitialisationForm()

    return render(request, 'jeu/nouveau.html', {'form': form})

def liste(request):

    elevages = Elevage.objects.all()

    return render(request, 'jeu/liste.html', {'elevages': elevages})


def elevage(request, elevage_id):
    elevage = get_object_or_404(Elevage, pk=elevage_id)
    individus = elevage.individus.all()

    if request.method == 'POST':
        form = TourActionForm(request.POST)
        if form.is_valid():
            actions = form.cleaned_data

            vendre_males = actions['vendre_males']
            vendre_femelles = actions['vendre_femelles']
            acheter_nourriture = actions['acheter_nourriture']
            acheter_cages = actions['acheter_cages']

            males = elevage.nombre_lapins_males
            femelles = elevage.nombre_lapins_femelles
            argent = elevage.argent

            erreurs = []
            if vendre_males > males:
                erreurs.append("Vous ne pouvez pas vendre plus de lapins mâles que vous n'en avez.")
            if vendre_femelles > femelles:
                erreurs.append("Vous ne pouvez pas vendre plus de femelles que vous n'en avez.")


            prix_vente_male = 1
            prix_vente_femelle = 1
            prix_nourriture = 1
            prix_cage = 1

            total_achats = acheter_nourriture * prix_nourriture + acheter_cages * prix_cage
            total_ventes = vendre_males * prix_vente_male + vendre_femelles * prix_vente_femelle

            if total_achats > argent + total_ventes:
                erreurs.append("Vous n'avez pas assez d'argent pour ces achats.")

            if erreurs:
                for erreur in erreurs:
                    form.add_error(None, erreur)
            else:
                # Mise à jour des ressources
                elevage.nombre_lapins_males -= vendre_males
                elevage.nombre_lapins_femelles -= vendre_femelles
                elevage.nourriture += acheter_nourriture
                elevage.cages += acheter_cages
                elevage.argent += total_ventes - total_achats

                elevage.save()
                return redirect('jeu:elevage_detail', elevage_id=elevage.id)
    else:
        form = TourActionForm()

    return render(request, 'jeu/elevage_detail.html', {
        'elevage': elevage,
        'individus': individus,
        'form': form,
    })
