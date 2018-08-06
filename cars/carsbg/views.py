from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from .models import *
from . import *
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib import messages
from ipware import get_client_ip

def home(request):
     return render(request, 'cars/home.html')

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return render(request, 'cars/home.html')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change.html', {
        'form': form
    })

def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('/')
	else:
		form = UserCreationForm()
	return render(request, 'registration/signup.html', {'form': form})

def service(request):
    return render(request, 'cars/serviceCreate.html')

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
			service = Service(name=name, city=city, address=address, tel=tel, typeOfObject = "Сервиз", image = img, rating = 0)	
			service.save()
		elif typeOfSearch == "cardealer":
			carDealer = CarDealer(name=name, city=city, address=address, tel=tel, typeOfObject = "Автокъща", image = img, rating = 0)
			carDealer.save()
		else:
			return HttpResponse("ERROR ^)^")

		return render(request, 'cars/home.html')

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

		return render(request, 'cars/results.html', {'results' : obj})

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


def objectCreate(request, comments, users, result, lenOfComments):
	
		name = request.POST.get('name', '')
		tel = request.POST.get('tel', '')
		address = request.POST.get('address', '')
		city = request.POST.get('city', '')
		typeOfObject = request.POST.get('typeOfObject', '')

		if typeOfObject == "Сервиз":
			result.append(Service.objects.filter(name = name, tel = tel, address = address, city = City.objects.filter(name = city)[0], typeOfObject = typeOfObject)[0])
			commentsObj = Comment.objects.filter(service = result[0])

		elif typeOfObject == "Автокъща":
			result.append(CarDealer.objects.filter(name = name, tel = tel, address = address, city = City.objects.filter(name = city)[0], typeOfObject = typeOfObject)[0])
			commentsObj = Comment.objects.filter(cardealer = result[0])

		for comment in commentsObj:
			comments.append(comment.text)
			users.append(comment.user)

		len1 = len(comments)
		for i in range(len1):
			lenOfComments.append(i)


@csrf_exempt
def viewObject(request):
	if request.POST:
		comments = []
		users = []
		result = list()
		lenOfComments = list()
		
		objectCreate(request, comments, users, result, lenOfComments)

		print(comments, users, result, lenOfComments)

		return render(request, 'cars/object.html', {'obj' : result[0], 'comments' : comments, 'lenOfComments' : lenOfComments, 'users' : users})


@csrf_exempt
def addComment(request):
	if request.POST:
		comment = request.POST.get('comment', '')
		user = request.POST.get('user', '')
		typeOfObject = request.POST.get('typeOfObject', '')
		pk = request.POST.get('pk', '')
		rating = int(request.POST.get('rating', ''))
		ip, is_routable = get_client_ip(request)
		limitExceeded = 0

		alert = ""


		if len(Comment.objects.filter(ip = ip)) > 2:
			limitExceeded = 1
		else:
			limitExceeded = 0

		print(len(Comment.objects.filter(ip = ip)), limitExceeded)
		if limitExceeded:
			alert = "Не можете да пишете повече коментари"


		if typeOfObject == "Сервиз" and limitExceeded == 0:
			obj = Service.objects.get(pk = pk)
			commentObj = Comment(text = comment, user = User.objects.filter(username = user)[0], service = obj, ip = ip)
			commentObj.save()
			

		elif typeOfObject == "Автокъща" and limitExceeded == 0:
			obj = CarDealer.objects.get(pk = pk)
			commentObj = Comment(text = comment, user = User.objects.filter(username = user)[0], cardealer = obj, ip = ip)
			commentObj.save()
		
		comments = []
		users = []
		result = list()
		lenOfComments = list()
		
		objectCreate(request, comments, users, result, lenOfComments)
		if limitExceeded == 0:
			result[0].rating = result[0].rating + rating
			result[0].save()
		print(ip)
		rating = result[0].rating / len(comments)
		return render(request, 'cars/object.html', {'obj' : result[0], 'comments' : comments, 'lenOfComments' : lenOfComments, 'users' : users, 'rating' : rating, 'alert' : alert})

