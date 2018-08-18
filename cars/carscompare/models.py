from django.db import models

class Brand(models.Model):
	name = models.CharField(max_length = 10)

	def __str__(self):
		return self.name

class ModelOfCar(models.Model):
	name = models.CharField(max_length = 10)
	brand = models.ForeignKey(Brand, on_delete = models.CASCADE, null = True)

	def __str__(self):
		return self.name

class Car(models.Model):

	# GEAR_CHOICES = [('1', 'AUTOMATIC'), ('2', 'MANUAL'), ('3', 'SEMIAUTO')]
	# UPHOLST_CHOICES = [('1', 'CLOTH'), ('2', 'LEATHER')]
	# ENGINE_CHOICES = [('1', 'DIESEL'), ('2', 'GASOLINE'), ('3', 'ELECTRIC')]


	brand = models.ForeignKey(Brand, on_delete = models.CASCADE, null = True)
	model = models.ForeignKey(ModelOfCar, on_delete = models.CASCADE, null = True)
	gear = models.CharField(max_length = 10)
	upholst = models.CharField(max_length = 10)
	year = models.CharField(max_length = 5)
	typeOfEngine = models.CharField(max_length = 10 	)
	price = models.CharField(max_length = 10)

	def __str__(self):
		return self.brand.name

