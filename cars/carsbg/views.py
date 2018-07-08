from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from .models import *
from . import *
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt


def home(request):
     return render(request, 'home.html')


def service(request):
    return render(request, 'serviceCreate.html')

@csrf_exempt
def addService(request):
	if request.method == 'POST':
		
		name = request.POST.get('name', '')
		cityName = request.POST.get('city', '')
		address = request.POST.get('address', '')
		tel = request.POST.get('tel', '')
		img = request.FILES.get('img', False)
		typeOfSearch = request.POST.get('type', '')

		if City.objects.filter(name=cityName):
			city = City.objects.filter(name=cityName)[0]
		else:
			city = City(name=cityName)
			city.save()
			
		if typeOfSearch == "service":
			service = Service(name=name, city=city, address=address, tel=tel, image = img)	
			service.save()
		elif typeOfSearch == "cardealer":
			carDealer = CarDealer(name=name, city=city, address=address, tel=tel, image = img)
			carDealer.save()
		else:
			return HttpResponse("ERROR ^)^")

		return render(request, 'home.html')

@csrf_exempt
def searchService(request):
	if request.method == 'POST':

		cityName = request.POST.get('city', '')
		city = City.objects.filter(name=cityName)[0]

		typeOfSearch = request.POST.get('type', '')

		if typeOfSearch == "service":
			obj = Service.objects.all().filter(city=city)
		elif typeOfSearch == "cardealer":
			obj = CarDealer.objects.all().filter(city = city)

		return render(request, 'results.html', {'results' : obj})
