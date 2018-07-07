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


		if City.objects.filter(name=cityName):
			service = Service(name=name, city = City.objects.filter(name=cityName)[0], address=address, tel=tel, image = img)
		else:
			city = City(name=cityName)
			city.save()
			service = Service(name=name, city=city, address=address, tel=tel, image = img)
			
		service.image = img

		service.save()

		return render(request, 'home.html')

@csrf_exempt
def searchService(request):
	if request.method == 'POST':

		cityName = request.POST.get('city', '')
		city = City.objects.filter(name=cityName)[0]

		typeOfSearch = request.POST.get('type', '')

		if typeOfSearch == "service":
			services = Service.objects.all().filter(city=city)
			return render(request, 'results.html', {'results' : services})

		return HttpResponse("TAPAK")