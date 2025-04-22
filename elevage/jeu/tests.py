from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Elevage, Individu, Regle
from .forms import InitialisationForm, TourActionForm

class ElevageTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Créer des règles de jeu par défaut
        Regle.objects.create(
            consommation_m1=0.0,
            consommation_m2=0.1,
            consommation_nourriture_adulte=0.25,
            max_par_portee=4,
            age_min_gravide=6,
            age_max_gravide=60,
            max_individus_par_cage=6,
            prix_vente_lapin=10,
            prix_nourriture=0.5,
            prix_cage=50
        )

    def test_elevage_creation(self):
        # Test de la création d'un élevage
        elevage = Elevage.objects.create(
            nom="Elevage Test",
            nourriture=10,
            cages=5,
            argent=100
        )

        self.assertEqual(elevage.nom, "Elevage Test")
        self.assertEqual(elevage.nourriture, 10)
        self.assertEqual(elevage.cages, 5)
        self.assertEqual(elevage.argent, 100)

    def test_initialisation_form_valid(self):
        # Test du formulaire d'initialisation avec des données valides
        data = {
            'nom': 'Elevage Test',
            'nb_lapins_males': 5,
            'nb_lapins_femelles': 5,
            'nourriture': 20,
            'nb_cages': 3,
            'argent': 50
        }
        form = InitialisationForm(data)
        self.assertTrue(form.is_valid())

    def test_initialisation_form_invalid(self):
        # Test du formulaire d'initialisation avec des données invalides
        data = {
            'nom': 'Elevage Test',
            'nb_lapins_males': -5,  # Nombre de mâles invalides
            'nb_lapins_femelles': 5,
            'nourriture': 20,
            'nb_cages': 3,
            'argent': 50
        }
        form = InitialisationForm(data)
        self.assertFalse(form.is_valid())

    def test_tour_action_form_valid(self):
        # Test du formulaire d'action de tour avec des données valides
        elevage = Elevage.objects.create(
            nom="Elevage Test",
            nourriture=20,
            cages=5,
            argent=100
        )
        form_data = {
            'vendre_males': 2,
            'vendre_femelles': 3,
            'acheter_nourriture': 500,
            'acheter_cages': 1
        }
        form = TourActionForm(form_data)
        self.assertTrue(form.is_valid())

    def test_elevage_view(self):
        # Test de la vue d'un élevage
        elevage = Elevage.objects.create(
            nom="Elevage Test",
            nourriture=20,
            cages=5,
            argent=100
        )
        url = reverse('jeu:elevage_detail', kwargs={'elevage_id': elevage.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Détails de l'élevage : Elevage Test")


    def test_initialisation_elevage_with_individus(self):
        # Test de l'initialisation d'un élevage avec des individus
        elevage = Elevage.objects.create(
            nom="Elevage Test",
            nourriture=20,
            cages=5,
            argent=100
        )
        for _ in range(5):
            Individu.objects.create(sexe='m', age=0, etat='present', elevage=elevage)
        for _ in range(5):
            Individu.objects.create(sexe='f', age=0, etat='present', elevage=elevage)

        self.assertEqual(elevage.nombre_lapins_males, 5)
        self.assertEqual(elevage.nombre_lapins_femelles, 5)

    def test_action_vendre_individus(self):
        # Test de la vente d'individus
        elevage = Elevage.objects.create(
            nom="Elevage Test",
            nourriture=20,
            cages=5,
            argent=100
        )
        for _ in range(5):
            Individu.objects.create(sexe='m', age=0, etat='present', elevage=elevage)
        for _ in range(5):
            Individu.objects.create(sexe='f', age=0, etat='present', elevage=elevage)

        data = {
            'vendre_males': 2,
            'vendre_femelles': 3,
            'acheter_nourriture': 100,
            'acheter_cages': 2
        }

        form = TourActionForm(data)
        form.is_valid()

        # Appliquer les changements après la vente
        elevage.argent += 2 * 5  # Prix de vente des mâles
        elevage.argent += 3 * 5  # Prix de vente des femelles

        self.assertEqual(elevage.argent, 100 + 10 + 15)

