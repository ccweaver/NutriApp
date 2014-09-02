from django.db import models
from Restaurant.models import Restaurant
from ingred_table.models import Ingredient

class Item(models.Model):
	name = models.CharField(max_length=100)
	rest_id = models.ForeignKey(Restaurant)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	ingredients = models.ManyToManyField(Ingredient)

	def __unicode__(self):
		return u'%s' % (self.name)