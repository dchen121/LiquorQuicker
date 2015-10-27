from django.db import models

# Create your models here.

class Location(models.Model):
	address = models.CharField(max_length=200)
	store_name = models.CharField(max_length=200)	

	def __str__(self):
		return self.store_name

