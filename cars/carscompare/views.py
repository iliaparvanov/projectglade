from django.shortcuts import render
from . import carsbg as cars
import json
from .models import *
from django.views.decorators.csrf import csrf_exempt
import time
import threading
import queue
import multiprocessing.pool as mpool
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from carsbg.models import *


def carsCompare(request):
	profile = 1
	if request.user.is_authenticated:
		profile = Profile.objects.get(user = request.user)
	return render(request, "carscompare/home.html", {"profile" : profile})

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
				print(Car.objects.get(brand = brandName, model = modelName, gear = info.get()[1][2], year = info.get()[1][3], price = info.get()[0], typeOfEngine = info.get()[1][4], image = info.get()[1][5]))

			except Car.DoesNotExist:
				car = Car(brand = brandName, model = modelName, gear = info.get()[1][2], year = info.get()[1][3], price = info.get()[0], typeOfEngine = info.get()[1][4], image = info.get()[1][5])
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
	rangeList = []
	for i in range(1972, 2018):
		rangeList.append(i)
	rangeList = list(reversed(rangeList))
	print(rangeList)
	profile = 1
	if request.user.is_authenticated:
		profile = Profile.objects.get(user = request.user)
	return render(request, "carscompare/home.html", {"brands" : brands, "range" : rangeList, "profile" : profile})

def displayModels(request):
	
	brand = request.GET.get('brand')
	models = ModelOfCar.objects.filter(brand = Brand.objects.filter(name = brand)[0])
	modelsList = []

	for i in models:
		modelsList.append(i.name)

	return JsonResponse({"models" : modelsList}, safe = False)

def displayCars(request):

	brand = request.POST.get('brandsId')
	model = request.POST.get('modelsId')
	gear = request.POST.get("gearId")
	year = request.POST.get("year")
	fuel = request.POST.get("fuelId")
	results = []
	cars = list(Car.objects.all())

	
	
	if brand != "Всички":
		cars = [i for i in cars if i.brand.name == brand]
				
	if model != "Всички":
		cars = [i for i in cars if i.model.name == model]

	if gear != "Всички":
		cars = [i for i in cars if i.gear == gear]

	if year != "Всички":
		cars = [i for i in cars if i.year == year]

	if fuel != "Всички":
		cars = [i for i in cars if i.fuel == fuel]
	
	

	for i in cars:
		results.append(i)
	profile = 1
	if request.user.is_authenticated:
		profile = Profile.objects.get(user = request.user)
	return render(request, "carscompare/results.html", {"results" : results, "profile" : profile})

def displayMore(request):
	brand = request.POST.get('brand')
	model = request.POST.get('model')
	gear = request.POST.get("gear")
	year = request.POST.get("year")
	fuel = request.POST.get("fuel")
	price = request.POST.get("price")

	car = Car.objects.filter(brand = Brand.objects.get(name = brand), model = ModelOfCar.objects.get(name = model), typeOfEngine = fuel, gear = gear, year = year, price = price)[0]
	profile = 1
	if request.user.is_authenticated:
		profile = Profile.objects.get(user = request.user)
	return render(request, "carscompare/car.html", {"car" : car, "profile" : profile})