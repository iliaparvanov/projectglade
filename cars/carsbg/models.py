from django.db import models
from django.contrib.auth.models import User

class City(models.Model):
	name = models.CharField(max_length = 15)

class Service(models.Model):
	name = models.CharField(max_length = 150)
	city = models.ForeignKey(City, on_delete = models.CASCADE, null=True)
	address = models.CharField(max_length = 100)
	tel = models.CharField(max_length = 100)
	image = models.ImageField(upload_to='media/', blank = True)
	typeOfObject = models.CharField(max_length = 100, null = True)
	rating = models.IntegerField()

class CarDealer(models.Model):
	name = models.CharField(max_length = 150, null = True)
	city = models.ForeignKey(City, on_delete = models.CASCADE)
	address = models.CharField(max_length = 100, null = True)
	tel = models.CharField(max_length = 100, null = True)
	image = models.ImageField(upload_to='media/', blank = True)
	typeOfObject = models.CharField(max_length = 100, null = True)
	rating = models.IntegerField()

class Comment(models.Model):
	text = models.CharField(max_length = 300, null = True)
	user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
	cardealer = models.ForeignKey(CarDealer, on_delete = models.CASCADE, null = True)
	service = models.ForeignKey(Service, on_delete = models.CASCADE, null = True)

class Car(models.Model):
	dealer = models.ForeignKey(CarDealer, on_delete = models.CASCADE)

