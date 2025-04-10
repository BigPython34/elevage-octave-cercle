from django.db import models


class Elevage(models.Model):
    nombre_lapins_males = models.IntegerField(default=0)  
    nombre_lapins_femelles = models.IntegerField(default=0)  
    nourriture = models.IntegerField(default=0)  
    argent = models.IntegerField(default=0)  
    cages = models.IntegerField(default=0)  
    nom = models.CharField(max_length=100, unique=True,default="Nom par défaut")
    
    def __str__(self):
        return self.nom


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
    
class Regle(models.Model):
    prix_nourriture = models.FloatField(default=0.5)  
    prix_cage = models.IntegerField(default=50)      
    prix_vente_lapin = models.IntegerField(default=10)  

    consommation_m1 = models.FloatField(default=0.0)   
    consommation_m2 = models.FloatField(default=0.1)   
    consommation_m3 = models.FloatField(default=0.25)  

    max_par_portee = models.IntegerField(default=4)
    max_individus_par_cage = models.IntegerField(default=6)

    age_min_gravide = models.IntegerField(default=6)    
    age_max_gravide = models.IntegerField(default=60)   
    duree_gestation = models.IntegerField(default=1)    

    def __str__(self):
        return "Règles du jeu"
