from django.db import models


class City(models.Model):
	name = models.CharField(max_length = 15)


class Service(models.Model):
	city = models.ForeignKey(City, on_delete = models.CASCADE)
	""" add more info.... """

class CarDealer(models.Model):
	city = models.ForeignKey(City, on_delete = models.CASCADE)

class Car(models.Model):
	dealer = models.ForeignKey(CarDealer, on_delete = models.CASCADE)
