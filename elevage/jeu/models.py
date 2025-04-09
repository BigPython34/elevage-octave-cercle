from django.db import models


class Elevage(models.Model):
    nombre_lapins_males = models.IntegerField(default=0)  
    nombre_lapins_femelles = models.IntegerField(default=0)  
    nourriture = models.IntegerField(default=0)  
    argent = models.IntegerField(default=0)  
    cages = models.IntegerField(default=0)  

    def __str__(self):
        return f"Elevage avec {self.nombre_lapins_males} mâles, {self.nombre_lapins_femelles} femelles, {self.cages} cages."

    def total_lapins(self):
        """
        Retourne le nombre total de lapins dans l'élevage (mâles + femelles).
        """
        return self.nombre_lapins_males + self.nombre_lapins_femelles