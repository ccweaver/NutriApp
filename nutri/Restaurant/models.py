from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
	name = models.CharField(max_length=300)
	cuisine1 = models.CharField(max_length=110)
	cuisine2 = models.CharField(max_length=110, null=True)
	cuisine3 = models.CharField(max_length=110, null=True)
	seamless = models.CharField(max_length=100, default='No')
	delivery_min = models.DecimalField(default=0.0, decimal_places=2, max_digits=5)
	number = models.IntegerField()
	street = models.CharField(max_length=300)
	city = models.CharField(max_length=300)
	state = models.CharField(max_length=100)
	#make this char field
	zipcode = models.CharField(max_length=15)
	hits = models.IntegerField(default=0)
	user = models.ForeignKey(User)
	website = models.CharField(max_length=300)
	yelp = models.CharField(max_length=300, default="")
	phone = models.BigIntegerField()
	moopen = models.CharField(max_length=300)
	moclose = models.CharField(max_length=300)
	tuopen = models.CharField(max_length=300)
	tuclose = models.CharField(max_length=300)
	weopen = models.CharField(max_length=300)
	weclose = models.CharField(max_length=300)
	thopen = models.CharField(max_length=300)
	thclose = models.CharField(max_length=300)
	fropen = models.CharField(max_length=300)
	frclose = models.CharField(max_length=300)
	saopen = models.CharField(max_length=300)
	saclose = models.CharField(max_length=300)
	suopen = models.CharField(max_length=300)
	suclose = models.CharField(max_length=300)
	
	def __unicode__(self):
		return u'%s' % (self.name)
	class Meta:
		db_table = 'restaurant_restaurant'
