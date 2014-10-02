from django.db import models
from ingred_table.models import Ingredient

class Addition(models.Model):
	ingred = models.ForeignKey(Ingredient)
	amount_grams = models.DecimalField(max_digits=10, decimal_places=2)

	def __unicode__(self):
		return u'%s' % (self.ingred)