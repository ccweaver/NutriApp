from django.db import models

class Ingredient(models.Model):
	ingredient = models.CharField(max_length=100)
	calories = models.DecimalField(max_digits=10, decimal_places=2)
	protein = models.DecimalField(max_digits=10, decimal_places=2)
	fat = models.DecimalField(max_digits=10, decimal_places=2)
	carbs = models.DecimalField(max_digits=10, decimal_places=2)
	sugar = models.DecimalField(max_digits=10, decimal_places=2)
	sodium = models.DecimalField(max_digits=10, decimal_places=2)

