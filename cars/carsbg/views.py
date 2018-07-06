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


		if City.objects.filter(name=cityName):
			service = Service(name=name, city=City.objects.filter(name=cityName), address=address, tel=tel)
		else:
			city = City(name=cityName)
			service = Service(name=name, city=city, address=address, tel=tel)
			city.save()

		service.save()

		return render(request, 'input.html')

@csrf_exempt
def searchService(request):
	if request.method == 'POST':

		cityName = request.POST.get('city', '')

		if City.objects.filter(name=cityName) == False:
			city = City(name=cityName)
			city.save()
		else:
			city = City.objects.filter(name=cityName)

		typeOfSearch = request.POST.get('type', '')

		if typeOfSearch == "service":
			services = Service.objects.all().filter(city=city[0])
			return render(request, 'results.html', {'results' : services})

		return HttpResponse("TAPAK")