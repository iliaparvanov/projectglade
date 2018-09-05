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
from django.utils import timezone
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.template.context_processors import csrf
from .forms import *


def home(request):
	form = MyRegistrationForm()
	return render(request, 'carsbg/home.html', {"form" : form})

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change.html', {
        'form': form
    })



def signup(request):
	if request.method == 'POST':
		form = MyRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('/')
		else:
			return render(request, 'registration/signup.html', {'form' : form})
	else:		
		form = MyRegistrationForm()
		return render(request, 'registration/signup.html', {'form' : form})

def service(request):
    return render(request, 'carsbg/serviceCreate.html')

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
			service = Object(name=name, city=city, address=address, tel=tel, typeOfObject = "Сервиз", image = img, rating = 0)
			service.save()
		elif typeOfSearch == "cardealer":
			carDealer = Object(name=name, city=city, address=address, tel=tel, typeOfObject = "Автокъща", image = img, rating = 0)
			carDealer.save()
		else:
			return HttpResponse("ERROR ^)^")

		return redirect('home')

@csrf_exempt
def searchService(request):
	if request.method == 'POST':

		searchWord = request.POST.get('search', '')
		obj = []
		

		if Object.objects.filter(name__icontains = searchWord, typeOfObject="Сервиз"):
			results = Object.objects.filter(name__icontains = searchWord, typeOfObject = "Сервиз").order_by("name")
			for i in results:
				if i not in obj:
					obj.append(i)

		if Object.objects.filter(name__icontains = searchWord, typeOfObject = "Автокъща"):
			results = Object.objects.filter(name__icontains = searchWord, typeOfObject = "Автокъща")
			for i in results:
				if i not in obj:
					obj.append(i)

		try:
			results = Object.objects.filter(city__name__icontains=City.objects.filter(name=searchWord)[0])

			for i in results:
				if i not in obj:
					obj.append(i)
		except IndexError:
			pass

		print(obj)
		return render(request, 'carsbg/results.html', {'results' : obj})

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

		suggestions = Object.objects.filter(name__icontains = term, typeOfObject = "Сервиз")
		for i in suggestions:
			suggestions_json = {}
			suggestions_json['label'] = i.name
			suggestions_json['category'] = "Сервизи:"

			results.append(suggestions_json)
			data = json.dumps(results)

		suggestions = Object.objects.filter(name__icontains = term, typeOfObject = "Автокъща")
		for i in suggestions:
			suggestions_json = {}
			suggestions_json['label'] = i.name
			suggestions_json['category'] = "Автокъщи:"

			results.append(suggestions_json)
			data = json.dumps(results)

		suggestions = Object.objects.filter(address__icontains = term)
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


def objectCreate(request, comments, result):

	if request.POST:
		name = request.POST.get('name')
		tel = request.POST.get('tel')
		address = request.POST.get('address')
		city = request.POST.get('city')
		typeOfObject = request.POST.get('typeOfObject')
		user = request.POST.get('user')

	elif request.GET:
		name = request.GET.get('name')
		tel = request.GET.get('tel')
		address = request.GET.get('address')
		city = request.GET.get('city')
		typeOfObject = request.GET.get('typeOfObject')
		user = request.POST.get('user')
	
	result.append(Object.objects.filter(name = name, tel = tel, address = address, city = City.objects.filter(name = city)[0], typeOfObject = typeOfObject)[0])
	currentUserComment = Comment.objects.filter(obj = result[0], user = User.objects.filter(username = user)[0])
	commentsObj = Comment.objects.filter(obj = result[0]).exclude(user = User.objects.filter(username = user)[0])

	# elif typeOfObject == "Автокъща":
	# 	result.append(Object.objects.filter(name = name, tel = tel, address = address, city = City.objects.filter(name = city).first(), typeOfObject = typeOfObject).first())
	# 	commentsObj = Comment.objects.filter(obj = result[0])

	for comment in currentUserComment:
		comments.append(comment)
	for comment in commentsObj:
		comments.append(comment)




def viewObject(request):

	comments = []	
	result = list()
	rating = 0
	alert = ''
	
	objectCreate(request, comments, result)
	print(comments)
	if len(comments) > 0:
		rating = result[0].rating / len(comments)
		rating = round(rating, 2)

	
	return render(request, 'carsbg/object.html', {'obj' : result[0], 'comments' : comments, "rating" : rating, 'alert' : alert})


@csrf_exempt
def addComment(request):
	if request.GET:
		comment = request.GET.get('comment', '')
		user = request.GET.get('user', '')
		typeOfObject = request.GET.get('typeOfObject', '')
		pk = request.GET.get('pk', '')
		rating = int(request.GET.get('rating', ''))

		print(comment, user)
		print("yeahhh")
		ip, is_routable = get_client_ip(request)

		limitExceeded = 0
		alert = ""
		obj = Object.objects.get(pk = pk, typeOfObject = typeOfObject)

		if len(Comment.objects.filter(obj = obj, ip = ip)) >= 1:
			limitExceeded = 1
			alert = "Вече оценихте този обект"

		

		count = 0
		for i in Comment.objects.filter(ip = ip):
				if i.date == timezone.now().date():
					count += 1
				print(timezone.now().date(), i.date)

		if count >= 4:
			limitExceeded = 1
			alert = "Днес надхвърлихте броя на позволените коментари"




		if limitExceeded == 0:

			commentObj = Comment(text = comment, user = User.objects.filter(username = user)[0], obj = obj, ip = ip, date = timezone.now().date(), rate = str(rating))
			commentObj.save()



		result = Object.objects.get(pk = pk, typeOfObject = typeOfObject)
		comments = Comment.objects.filter(obj = result)
		print(result)
		if limitExceeded == 0:
			result.rating = result.rating + rating
			result.save()

		if len(comments) > 0:
			rating = result.rating / len(comments)

	
	return JsonResponse({"alert" : alert}, safe = False)

def deleteComment(request):
	user = request.GET.get('user')
	pk = request.GET.get('pk')

	comment = Comment.objects.get(obj = Object.objects.get(pk = pk), user = User.objects.get(username = user))
	obj = Object.objects.get(pk = pk)
	obj.rating -= int(comment.rate)

	if obj.rating < 0:
		obj.rating = 0

	obj.save()
	comment.delete()
	return JsonResponse("Success", safe = False)