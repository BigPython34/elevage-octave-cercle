from django.db import models
import random
class Regle(models.Model):
    prix_nourriture = models.FloatField(default=0.5)  
    prix_cage = models.IntegerField(default=50)      
    prix_vente_lapin = models.IntegerField(default=10)  

    consommation_m1 = models.FloatField(default=0.0)   
    consommation_m2 = models.FloatField(default=0.1)   
    consommation_m3 = models.FloatField(default=0.25)  
    consommation_nourriture_adulte=models.FloatField(default=0.25)
    max_par_portee = models.IntegerField(default=4)
    max_individus_par_cage = models.IntegerField(default=6)

    age_min_gravide = models.IntegerField(default=6)    
    age_max_gravide = models.IntegerField(default=60)   
    duree_gestation = models.IntegerField(default=1)    

    def __str__(self):
        return "Règles du jeu"
    
class Elevage(models.Model): 
    nourriture = models.IntegerField(default=0)  
    argent = models.IntegerField(default=0)  
    cages = models.IntegerField(default=0)  
    nom = models.CharField(max_length=100, unique=True, default="Nom par défaut")
    regle = models.ForeignKey('Regle', on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def nombre_lapins_males(self):
        return self.individus.filter(sexe='m', etat='present').count()

    @property
    def nombre_lapins_femelles(self):
        return self.individus.filter(sexe='f', etat='present').count()

    def __str__(self):
        return self.nom

    def avancer_tour(self):
        regle = self.regle
        if not regle:
            return "Aucune règle définie pour cet élevage."

        # Étape 1 : Préparer la liste des individus avec leur consommation
        individus_consommation = []
        for individu in self.individus.filter(etat='present'):
            if individu.age == 1:
                conso = regle.consommation_m1
            elif individu.age == 2:
                conso = regle.consommation_m2
            else:
                conso = regle.consommation_nourriture_adulte
            individus_consommation.append((conso, individu))

        # Étape 2 : Trier les individus par consommation croissante
        individus_consommation.sort(key=lambda x: x[0])

        # Étape 3 : Nourrir ce qu'on peut
        nourriture_disponible = self.nourriture
        total_nourriture_utilisee = 0

        for conso, individu in individus_consommation:
            if nourriture_disponible >= conso:
                nourriture_disponible -= conso
                total_nourriture_utilisee += conso
            else:
                individu.etat = 'mort'
                individu.save()

        # Étape 4 : Reproduction
        femelles_reproductrices = self.individus.filter(
            sexe='f',
            etat='present',
            age__gte=regle.age_min_gravide,
            age__lte=regle.age_max_gravide
        )
        for femelle in femelles_reproductrices:
            if femelle.age >= 6:
                nombre_lapereaux = random.randint(1, regle.max_par_portee)
                for _ in range(nombre_lapereaux):
                    sexe = random.choice(['m', 'f'])
                    Individu.objects.create(
                        sexe=sexe,
                        age=0,
                        etat='present',
                        elevage=self
                    )

        # Étape 5 : Surpopulation
        total_individus = self.individus.filter(etat='present').count()
        capacite_max = self.cages * regle.max_individus_par_cage

        if total_individus > capacite_max:
            excedent = total_individus - capacite_max
            individus_a_mourir = self.individus.filter(etat='present')[:excedent]
            for individu in individus_a_mourir:
                individu.etat = 'mort'
                individu.save()

        # Étape 6 : Vieillissement
        for individu in self.individus.filter(etat='present'):
            individu.age += 1
            individu.save()

        # Mise à jour des ressources
        self.nourriture -= total_nourriture_utilisee
        self.save()

        return "Tour terminé avec succès."

class Individu(models.Model):
    ETAT_CHOICES = [
        ('present', 'Présent'),
        ('vendu', 'Vendu'),
        ('mort', 'Mort'),
        ('gravide', 'Gravide'),
    ]

    SEXE_CHOICES = [
        ('m', 'Mâle'),
        ('f', 'Femelle'),
    ]

    elevage = models.ForeignKey(Elevage, on_delete=models.CASCADE, related_name='individus')
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    age = models.IntegerField()  
    etat = models.CharField(max_length=7, choices=ETAT_CHOICES, default='present')
    

