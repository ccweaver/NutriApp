from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
	name = models.CharField(max_length=300)
	cuisine1 = models.CharField(max_length=110)
	cuisine2 = models.CharField(max_length=110, null=True)
	cuisine3 = models.CharField(max_length=110, null=True)
	seamless = models.CharField(max_length=100, default='No')
	delivery_min = models.IntegerField(default="")
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
	moopen = models.DateTimeField()
	moclose = models.DateTimeField()
	tuopen = models.DateTimeField()
	tuclose = models.DateTimeField()
	weopen = models.DateTimeField()
	weclose = models.DateTimeField()
	thopen = models.DateTimeField()
	thclose = models.DateTimeField()
	fropen = models.DateTimeField()
	frclose = models.DateTimeField()
	saopen = models.DateTimeField()
	saclose = models.DateTimeField()
	suopen = models.DateTimeField()
	suclose = models.DateTimeField()
	
	def __unicode__(self):
		return u'%s' % (self.name)
	class Meta:
		db_table = 'restaurant_restaurant'
