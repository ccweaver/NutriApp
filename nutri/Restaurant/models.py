from django.db import models

class Restaurant(models.Model)
	name = models.CharField(max_length=300)
	number = models.IntegerField(max_digits=10)
	street = models.CharField(max_length=300)
	city = models.CharField(max_length=300)
	state = models.CharField(max_length=100)
	zipcode = models.IntegerField(max_digits=10)
