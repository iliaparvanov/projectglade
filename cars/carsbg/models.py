from django.db import models
from django.contrib.auth.models import User
#from django_google_maps import fields as map_fields

"""class Rental(models.Model):
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)
"""
class City(models.Model):
	name = models.CharField(max_length = 15)

	def __str__(self):
		return self.name

class Object(models.Model):
	name = models.CharField(max_length = 150)
	city = models.ForeignKey(City, on_delete = models.CASCADE, null=True)
	address = models.CharField(max_length = 100)
	tel = models.CharField(max_length = 100)
	image = models.ImageField(upload_to='media/', blank = True)
	typeOfObject = models.CharField(max_length = 100, null = True)
	rating = models.IntegerField()

	def __str__(self):
		return self.name 

# class CarDealer(models.Model):
# 	name = models.CharField(max_length = 150, null = True)
# 	city = models.ForeignKey(City, on_delete = models.CASCADE)
# 	address = models.CharField(max_length = 100, null = True)
# 	tel = models.CharField(max_length = 100, null = True)
# 	image = models.ImageField(upload_to='media/', blank = True)
# 	typeOfObject = models.CharField(max_length = 100, null = True)
# 	rating = models.IntegerField()

# 	def __str__(self):
# 		return self.name

class Comment(models.Model):
	text = models.CharField(max_length = 300, null = True)
	user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
	obj = models.ForeignKey(Object, on_delete = models.CASCADE, null = True)
	ip = models.CharField(max_length=15, null = True)
	date = models.DateField(null=True)

	def __str__(self):
		return self.text + str(self.date)
