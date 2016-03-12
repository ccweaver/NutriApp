from django.db import models
from ingred_table.models import Ingredient

class PreValue(models.Model):
	ingredID = models.ForeignKey(Ingredient)
	saladGrams = models.DecimalField(max_digits=10, decimal_places=2)
	wrapGrams = models.DecimalField(max_digits=10, decimal_places=2)
	tomatoMozzGrams = models.DecimalField(max_digits=10, decimal_places=2)
	
	def __unicode__(self):
		return u'%s' % (self.name)
