from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from .models import *
from . import *
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
import json

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
			service = Service(name=name, city=city, address=address, tel=tel, typeOfObject = "Сервиз", image = img)	
			service.save()
		elif typeOfSearch == "cardealer":
			carDealer = CarDealer(name=name, city=city, address=address, tel=tel, typeOfObject = "Автокъща", image = img)
			carDealer.save()
		else:
			return HttpResponse("ERROR ^)^")

		return render(request, 'home.html')

@csrf_exempt
def searchService(request):
	if request.method == 'POST':

		searchWord = request.POST.get('search', '')
		obj = []
		if City.objects.filter(name=searchWord):
			results = Service.objects.all().filter(city=City.objects.filter(name=searchWord)[0])
			obj.append(results)

			results = CarDealer.objects.all().filter(city=City.objects.filter(name=searchWord)[0])
			if results not in obj:
				obj.append(results)

		if Service.objects.filter(name = searchWord):
			results = Service.objects.filter(name = searchWord)
			if results not in obj:
				obj.append(results)

		if CarDealer.objects.filter(name = searchWord):
			results = CarDealer.objects.filter(name = searchWord)
			if results not in obj:
				obj.append(results)

		return render(request, 'results.html', {'results' : obj})

	if request.is_ajax():
        
		term = request.GET.get('term', '')
		suggestions = City.objects.filter(name__icontains = term)
		results = []
		for i in suggestions:
			suggestions_json = {}
			suggestions_json['label'] = i.name
			suggestions_json['category'] = "Градове:"

			results.append(suggestions_json)
			data = json.dumps(results)

		suggestions = Service.objects.filter(name__icontains = term)
		for i in suggestions:
			suggestions_json = {}
			suggestions_json['label'] = i.name
			suggestions_json['category'] = "Сервизи:"

			results.append(suggestions_json)
			data = json.dumps(results)

		suggestions = CarDealer.objects.filter(name__icontains = term)
		for i in suggestions:
			suggestions_json = {}
			suggestions_json['label'] = i.name
			suggestions_json['category'] = "Автокъщи:"

			results.append(suggestions_json)
			data = json.dumps(results)

		suggestions = Service.objects.filter(address__icontains = term)
		for i in suggestions:
			suggestions_json = {}
			suggestions_json['label'] = i.name
			suggestions_json['category'] = "Местоположение:"

			results.append(suggestions_json)
			data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'
	
	return HttpResponse(data, mimetype)