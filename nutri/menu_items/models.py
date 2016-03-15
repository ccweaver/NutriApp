from django.db import models
from Restaurant.models import Restaurant
from added_ingreds.models import Addition
from django.contrib.auth.models import User


class Item(models.Model):
	name = models.CharField(max_length=100)
	rest = models.ForeignKey(Restaurant)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	ingredients = models.ManyToManyField(Addition, blank=True)
	valid = models.BooleanField(default=False)
	description = models.TextField()
	calories = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=True)
	protein = models.DecimalField(max_digits=8, decimal_places=2, default=-1, null=True)
	fat = models.DecimalField(max_digits=8, decimal_places=2, default=-1, null=True)
	carbs = models.DecimalField(max_digits=8, decimal_places=2, default=-1, null=True)
	sugar = models.DecimalField(max_digits=8, decimal_places=2, default=-1, null=True)
	sodium = models.DecimalField(max_digits=8, decimal_places=2, default=-1, null=True)
	likes = models.ManyToManyField(User, blank=True)

	def __unicode__(self):
		return u'%s' % (self.name)