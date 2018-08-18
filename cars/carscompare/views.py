from django.shortcuts import render
from .scraper import carsbg as cars
from .scraper import maps
from .models import *
from django.views.decorators.csrf import csrf_exempt
import time


def carsCompare(request):
	return render(request, "carscompare/home.html")

@csrf_exempt
def addCars(request):

	index = 0
	for brand, brandid in maps.brandId.items():
		for model, modelid in maps.globalsFromMaps[brand].items():
			for gear, gearid in maps.gearId.items():
				for fuel, fuelId in maps.fuelId.items():
					for yearid in maps.yearid:


						if yearid < 2006 and fuelId == 7:
							print("skip")
						else:

							time.sleep(1)
							avgPrice = cars.scraper(str(brandid), str(modelid), str(gearid), str(yearid), str(fuelId))
							print(brand, gear, model, fuel, yearid, index)
							if avgPrice != []:
								try:
									brandName = Brand.objects.get(name = brand)

								except Brand.DoesNotExist:
									brandName = Brand(name = brand)
									brandName.save()
								
								try:
									modelName = ModelOfCar.objects.get(name = model)
								except ModelOfCar.DoesNotExist:
									modelName = ModelOfCar(name = model)
									modelName.save()

								try:
									Car.objects.get(brand = brandName, model = modelName, gear = gear, year = yearid, price = avgPrice, typeOfEngine = fuel)
								except Car.DoesNotExist:
									Car(brand = brandName, model = modelName, gear = gear, year = yearid, price = avgPrice, typeOfEngine = fuel)
									car.save()
									index += 1

		
	return render(request, "carscompare/home.html")
