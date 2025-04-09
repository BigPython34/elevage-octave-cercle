from django.db import models


class Elevage(models.Model):
    nombre_lapins_males = models.IntegerField(default=0)  
    nombre_lapins_femelles = models.IntegerField(default=0)  
    nourriture = models.IntegerField(default=0)  
    argent = models.IntegerField(default=0)  
    cages = models.IntegerField(default=0)  
    nom = models.CharField(max_length=100, unique=True,default="Nom par défaut")
    def __str__(self):
        return self.nom+f"  avec {self.nombre_lapins_males} mâles, {self.nombre_lapins_femelles} femelles, {self.cages} cages."


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