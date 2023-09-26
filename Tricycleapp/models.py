from django.db import models
from django.urls import reverse
from datetime import date
from django.conf import settings
# Create your models here.


class Modele(models.Model):
	name = models.CharField(max_length=120)
		
	def __str__(self):
		return self.name

class Tricycle(models.Model):
    modele = models.ForeignKey(Modele, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=19, decimal_places=2, default=2000.00) 
    weight = models.CharField(max_length=120)
    image = models.FileField(upload_to='uploads/')

    def get_absolute_url(self):
        return reverse('tricycle:detail', kwargs={'pk': self.pk})
    
    def __str__(self):
    	return f'{self.modele} {self.name}'
    
    
    

class Reservation(models.Model):
    modele = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    #price = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    adress = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    montant_restant = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tranche = models.CharField(max_length=15,default="paiement")
    nouveau_prix = models.DecimalField(max_digits=10, decimal_places=2,default="0000")
    apayer = models.DecimalField(max_digits=10, decimal_places=2,default="0000")
    phone = models.CharField(max_length=20,default=00000000)
    paye = models.BooleanField(default=False)
