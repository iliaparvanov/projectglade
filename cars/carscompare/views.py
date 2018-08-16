from django.shortcuts import render
from .scraper import autoscout24 as auto
from .models import *
from django.views.decorators.csrf import csrf_exempt


def carsCompare(request):
	return render(request, "carscompare/home.html")

@csrf_exempt
def addCars(request):
	brand = Brand(name = auto.brand)
	brand.save()
	
	model = ModelOfCar(name = auto.model)
	model.save()

	car = Car(brand = brand, model = model, gear = auto.gear, upholst = auto.upholstery, year = auto.year, price = auto.prices, typeOfEngine = auto.fuel)
	car.save()
	return render(request, "carscompare/home.html")
