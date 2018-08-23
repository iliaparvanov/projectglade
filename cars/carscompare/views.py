from django.shortcuts import render
from . import carsbg as cars

from .models import *
from django.views.decorators.csrf import csrf_exempt
import time
import threading
import queue
import multiprocessing.pool as mpool


def carsCompare(request):
	return render(request, "carscompare/home.html")

def addCarToDb(info):
	print(info.get())
	if info.get()[0] != []:
			try:
				brandName = Brand.objects.get(name = info.get()[1][0])

			except Brand.DoesNotExist:
				brandName = Brand(name = info.get()[1][0])
				brandName.save()
			
			try:
				modelName = ModelOfCar.objects.get(name = info.get()[1][1], brand = brandName)

			except ModelOfCar.DoesNotExist:
				modelName = ModelOfCar(name = info.get()[1][1], brand = brandName)
				modelName.save()

			try:
				print(Car.objects.get(brand = brandName, model = modelName, gear = info.get()[1][2], year = info.get()[1][3], price = info.get()[0], typeOfEngine = info.get()[1][4]))

			except Car.DoesNotExist:
				car = Car(brand = brandName, model = modelName, gear = info.get()[1][2], year = info.get()[1][3], price = info.get()[0], typeOfEngine = info.get()[1][4])
				car.save()
			print("DONEEEEEEEEEEEEEEEEE")


@csrf_exempt
def addCars(request):

	urls = list()
	urls = cars.urlsCreate()
	pool = mpool.ThreadPool(5)
	print(len(urls))
	info = [pool.apply_async(cars.scraper, (url[0], url[1])) for url in urls]
	
	pool.close()
	pool.join()	

	for i in info:
		addCarToDb(i)

	return render(request, "carscompare/home.html")

def displayCarsProperties(request):
	brands = Brand.objects.all()

	return render(request, "carscompare/home", {"brands" : brands})

def displayModels(request):
	if request.POST:

		brands = request.POST.get('brand')
		models = ModelOfCar.objects.filter(brand = Brand.objects.filter(name = brand))
		
		return render(request, "carscompare/home.html", {"models" : models})	
