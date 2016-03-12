from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
	name = models.CharField(max_length=300)
	cuisine1 = models.CharField(max_length=110, null=True)
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
	neighborhood = models.CharField(max_length=100, default='')
	hits = models.IntegerField(default=0)
	user = models.ForeignKey(User)
	website = models.CharField(max_length=300, null=True)
	yelp = models.CharField(max_length=300, default="", null=True)
	phone = models.BigIntegerField(null=True)
	hours = models.CharField(max_length=300, default="", null=True)
	moopen = models.CharField(max_length=300, null=True)
	moclose = models.CharField(max_length=300, null=True)
	tuopen = models.CharField(max_length=300, null=True)
	tuclose = models.CharField(max_length=300, null=True)
	weopen = models.CharField(max_length=300, null=True)
	weclose = models.CharField(max_length=300, null=True)
	thopen = models.CharField(max_length=300, null=True)
	thclose = models.CharField(max_length=300, null=True)
	fropen = models.CharField(max_length=300, null=True)
	frclose = models.CharField(max_length=300, null=True)
	saopen = models.CharField(max_length=300, null=True)
	saclose = models.CharField(max_length=300, null=True)
	suopen = models.CharField(max_length=300, null=True)
	suclose = models.CharField(max_length=300, null=True)
	
	def __unicode__(self):
		return u'%s' % (self.name)
	class Meta:
		db_table = 'restaurant_restaurant'
