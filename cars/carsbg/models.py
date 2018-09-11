from django.db import models
from django.contrib.auth.models import User
#from django_google_maps import fields as map_fields

"""class Rental(models.Model):
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)
"""

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE, null = True)
	image = models.ImageField(upload_to='media/', blank = True)

	def __str__(self):
		return self.user.username

class City(models.Model):
	name = models.CharField(max_length = 15)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ["name"]

class WorkingTime(models.Model):
	dayWork = models.CharField(max_length = 30)
	saturday = models.CharField(max_length = 30)
	sunday = models.CharField(max_length = 30)



class Object(models.Model):
	name = models.CharField(max_length = 150)
	city = models.ForeignKey(City, on_delete = models.CASCADE, null=True)
	address = models.CharField(max_length = 100)
	tel = models.CharField(max_length = 100)
	image = models.ImageField(upload_to='media/', blank = True)
	typeOfObject = models.CharField(max_length = 100, null = True)
	rating = models.IntegerField()
	description = models.CharField(max_length = 600, null = True)
	workingTime = models.ForeignKey(WorkingTime, on_delete = models.CASCADE, null = True)

	def __str__(self):
		return self.name 

	class Meta:
		ordering = ["rating", "name"]

class Comment(models.Model):
	text = models.CharField(max_length = 300, null = True)
	user = models.ForeignKey(Profile, on_delete = models.CASCADE, null = True)
	obj = models.ForeignKey(Object, on_delete = models.CASCADE, null = True)
	ip = models.CharField(max_length=15, null = True)
	date = models.DateField(null=True)
	rate = models.CharField(max_length = 6, null = True)

	def __str__(self):
		return str(self.user.user.username) + " " + str(self.date)

	class Meta:
		ordering = ["date", "user"]

	
class Service(models.Model):
	obj = models.ManyToManyField(Object, null = True)
	name = models.CharField(max_length = 100)
	description = models.CharField(max_length = 600)
	image = models.ImageField(upload_to='media/', blank = True)
	icon = models.ImageField(upload_to='media/', blank = True)

	def __str__(self):
		return str(self.name)

	class Meta:
		ordering = ["name"]