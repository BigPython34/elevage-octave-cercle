from django.shortcuts import render, redirect,get_object_or_404
from .forms import InitialisationForm,TourActionForm
from .models import Elevage,Individu,Regle
from django.contrib import messages

def accueil(request):
    return render(request, 'jeu/accueil.html')

def confirmation(request):

    return render(request, 'jeu/confirmation.html')  

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
    individus = elevage.individus.filter(etat='present')
    regle = elevage.regle

    if request.method == 'POST':
        form = TourActionForm(request.POST)
        if form.is_valid():
            actions = form.cleaned_data

            vendre_males = actions['vendre_males']
            vendre_femelles = actions['vendre_femelles']
            acheter_nourriture = actions['acheter_nourriture']
            acheter_cages = actions['acheter_cages']

            erreurs = []

            lapins_males = individus.filter(sexe='m').count()
            lapins_femelles = individus.filter(sexe='f').count()

            if vendre_males > lapins_males:
                erreurs.append("Vous ne pouvez pas vendre plus de lapins mâles que vous n'en avez.")
            if vendre_femelles > lapins_femelles:
                erreurs.append("Vous ne pouvez pas vendre plus de femelles que vous n'en avez.")

            if not regle:
                erreurs.append("Aucune règle définie pour cet élevage.")
            else:
                prix_vente = regle.prix_vente_lapin
                prix_nourriture = regle.prix_nourriture
                prix_cage = regle.prix_cage
                total_ventes=(vendre_males+vendre_femelles)*prix_vente
                total_achats = 0.001 * acheter_nourriture * prix_nourriture + acheter_cages * prix_cage

                if total_achats > elevage.argent+total_ventes:
                    erreurs.append("Vous n'avez pas assez d'argent pour ces achats.")

            if erreurs:
                for erreur in erreurs:
                    form.add_error(None, erreur)
            else:
                # Appliquer les achats (via avancer_tour)
                elevage.nourriture += 0.001*acheter_nourriture
                elevage.cages += acheter_cages
                elevage.avancer_tour()


                males_a_vendre = list(individus.filter(sexe='m')[:vendre_males])
                femelles_a_vendre = list(individus.filter(sexe='f')[:vendre_femelles])
                individus_a_vendre = males_a_vendre + femelles_a_vendre

                for individu in individus_a_vendre:
                    individu.etat = 'vendu'
                    individu.save()

                elevage.argent += total_ventes-total_achats
                elevage.save()

                return redirect('jeu:elevage_detail', elevage_id=elevage.id)
    else:
        form = TourActionForm()

    return render(request, 'jeu/elevage_detail.html', {
        'elevage': elevage,
        'individus': individus,
        'form': form,
    })
