from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
	name = models.CharField(max_length=300)
	number = models.IntegerField()
	street = models.CharField(max_length=300)
	city = models.CharField(max_length=300)
	state = models.CharField(max_length=100)
	zipcode = models.IntegerField()
	user = models.ForeignKey(User)
	website = models.CharField(max_length=300)
	phone = models.IntegerField()
	

	def __unicode__(self):
		return u'%s' % (self.name)
	class Meta:
		db_table = 'restaurant_restaurant'
