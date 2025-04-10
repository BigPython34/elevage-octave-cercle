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
    nom = models.CharField(max_length=100, unique=True,default="Nom par défaut")
    regle = models.ForeignKey(Regle, on_delete=models.SET_NULL, null=True, blank=True)
    @property
    def nombre_lapins_males(self):

        return self.individus.filter(sexe='m', etat='present').count()

    @property
    def nombre_lapins_femelles(self):

        return self.individus.filter(sexe='f', etat='present').count()
    def __str__(self):
        return self.nom

    def set_nombre_lapins_males(self, nombre):

        self.nombre_lapins_males = nombre

    def set_nombre_lapins_femelles(self, nombre):

        self.nombre_lapins_femelles = nombre
    
    def avancer_tour(self, actions_saisies):


        regle = self.regle
        
        if not regle:
            return "Aucune règle définie pour cet élevage."


        total_nourriture_requise = 0
        
        total_nourriture_requise += self.nombre_lapins_males * regle.consommation_nourriture_adulte
        total_nourriture_requise += self.nombre_lapins_femelles * regle.consommation_nourriture_adulte
        

        for individu in self.individus.filter(etat='present'):
            if individu.age == 1:
                total_nourriture_requise += regle.consommation_m1
                continue
            elif individu.age == 2:

                total_nourriture_requise += regle.consommation_m2
            elif individu.age >= 3:

                total_nourriture_requise += regle.consommation_nourriture_adulte
        

        if self.nourriture < total_nourriture_requise:

            individus_a_mourir = self.individus.filter(etat='present')[:self.individus.count() - (self.nourriture // regle.consommation_nourriture_adulte)]
            for individu in individus_a_mourir:
                individu.etat = 'mort'
                individu.save()


        femelles_reproductrices = self.individus.filter(sexe='f', etat='present', age__gte=regle.age_min_gravide, age__lte=regle.age_max_gravide)
        for femelle in femelles_reproductrices:

            if femelle.age >= 6:
                nombre_lapereaux = random.randint(1, regle.max_par_portee)  
                sexe_lapereaux = random.choice(['m', 'f'])  


                for _ in range(nombre_lapereaux):
                    Individu.objects.create(
                        sexe=sexe_lapereaux,
                        age=0,  
                        etat='present',
                        elevage=self
                    )
        

        total_individus = self.individus.filter(etat='present').count()
        if total_individus > self.cages * regle.max_individus_par_cage:

            excedent = total_individus - self.cages * regle.max_individus_par_cage
            individus_a_mourir = self.individus.filter(etat='present')[:excedent]
            for individu in individus_a_mourir:
                individu.etat = 'mort'
                individu.save()
        

        for individu in self.individus.filter(etat='present'):
            individu.age += 1
            individu.save()


        self.nourriture -= total_nourriture_requise
        self.argent -= actions_saisies['argent_dépensé']  


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
    

