from django.db import models

class Restaurant(models.Model):
	name = models.CharField(max_length=300)
	number = models.IntegerField()
	street = models.CharField(max_length=300)
	city = models.CharField(max_length=300)
	state = models.CharField(max_length=100)
	zipcode = models.IntegerField()

	def __unicode__(self):
		return u'%s' % (self.name)
	class Meta:
		db_table = 'restaurant_restaurant'
