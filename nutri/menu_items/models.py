from django.db import models
from Restaurant.models import Restaurant
from added_ingreds.models import Addition

class Item(models.Model):
	name = models.CharField(max_length=100)
	rest = models.ForeignKey(Restaurant)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	ingredients = models.ManyToManyField(Addition, blank=True)
	valid = models.BooleanField(default=False)
	description = models.TextField()
	calories = models.DecimalField(max_digits=10, decimal_places=2, default=0)

	def __unicode__(self):
		return u'%s' % (self.name)