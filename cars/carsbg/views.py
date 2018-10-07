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
from social_django.models import UserSocialAuth
from django.contrib.auth import logout

def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'carsbg/settings.html', {
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'core/password.html', {'form': form})


def home(request):
	form = MyRegistrationForm()
	flagForBase = 1
	profile = 1
	if request.user.is_authenticated:
		profile = Profile.objects.get(user = request.user)
		
	return render(request, 'carsbg/home.html', {"form" : form, "flagForBase" : flagForBase, "profile" : profile})

def login_user(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
        else:
            form = MyRegistrationForm()
            return render(request, "carsbg/home.html", {"errorFlagLogin" : 1, "profile" : profile, "form" : form})
    else:
    	return redirect('/')


@login_required
def password_change(request):
    if request.method == 'POST':
        form = MyPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = MyPasswordChangeForm(request.user)
        print(form)
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
			profile = Profile(user = user)
			profile.save()
			return redirect('/')
		else:
			return render(request, 'carsbg/home.html', {'form' : form, 'errorFlagSignup' : 1})
	else:		
		form = MyRegistrationForm()
		return render(request, 'carsbg/home.html', {'form' : form})

def profile(request):
	profile = 1
	if request.user.is_authenticated:
		profile = Profile.objects.get(user = request.user)
	return render(request, "registration/signup.html", {"profile" : profile})

def setImage(request):
	if request.method == 'POST':
		user = request.POST.get('user')
		image = request.FILES.get('img', False)
		profile = Profile.objects.get(user = User.objects.get(username = user))
		profile.image = image
		profile.save()

	return redirect('/')

def object(request):
	form = MyRegistrationForm()
	profile = 1
	if request.user.is_authenticated:
		profile = Profile.objects.get(user = request.user)

	services = Service.objects.all()
	return render(request, 'carsbg/serviceCreate.html', {'form' : form, "profile" : profile, "services" : services})

@csrf_exempt
def addService(request):
	if request.method == 'POST':

		name = request.POST.get('name', '')
		cityName = request.POST.get('city', '')
		address = request.POST.get('address', '')
		tel = request.POST.get('tel', '')
		img = request.FILES.get('img')
		typeOfObject = request.POST.get('type', '')
		workdayStart = request.POST.get('workdayStart')
		workdayEnd = request.POST.get('workdayEnd')
		saturdayStart = request.POST.get('saturdayStart')
		saturdayEnd = request.POST.get('saturdayEnd')
		
		description = request.POST.get('description')

		workday = str(workdayStart) + ' - ' + str(workdayEnd)
		saturday = str(saturdayStart) + ' - ' + str(saturdayEnd)
		sunday = "Затворено"
		workingTime = WorkingTime(dayWork = workday, sunday = sunday, saturday = saturday)
		workingTime.save()

		services = request.POST.getlist('multipleSelect', '')


		if City.objects.filter(name=cityName):
			city = City.objects.filter(name=cityName)[0]
		else:
			city = City(name=cityName)
			city.save()

		
		obj1 = Object(name=name, city=city, address=address, tel=tel, typeOfObject = typeOfObject, image = img, rating = 0, workingTime = workingTime, description = description)
		obj1.save()
		


		for i in services:
			service = Service.objects.get(name = str(i))
			service.obj.add(obj1)
			service.save()

		return redirect('home')

def search(request):
	city = City.objects.all()
	objects = Object.objects.all()
	types = []
	for i in objects:
		if i.typeOfObject not in types:
			types.append(i.typeOfObject)

	form = MyRegistrationForm()
	profile = 1
	if request.user.is_authenticated:
		profile = Profile.objects.get(user = request.user)


	return render(request, "carsbg/search.html", {"city" : city, "types" : types, "form" : form, "profile" : profile})

@csrf_exempt
def searchService(request):
	
	if request.method == 'POST':

		searchWord = request.POST.get('search', '')
		typeOfObject = request.POST.get('typeOfObject', '')
		rating = request.POST.get('ratingId', '')
		city = request.POST.get('cityId', '')
		obj = []
		print(rating)
		
		if Object.objects.filter(name__icontains = searchWord):
			results = Object.objects.filter(name__icontains = searchWord).order_by("name")
			for i in results:
				if i not in obj:
					obj.append(i)

		

		if Object.objects.filter(address__icontains = searchWord):
			results = Object.objects.filter(address__icontains = searchWord).order_by("name")
			for i in results:
				if i not in obj:
					obj.append(i)

		if (str(obj[3].ratingDisplay) == rating):
			print(obj[3].ratingDisplay, rating)

		if typeOfObject != "Всички":
			obj = [i for i in obj if i.typeOfObject == typeOfObject]
				
		if rating != "Всички":
			оbj = [i for i in obj if i.ratingDisplay == int(rating)]

		if city != "Всички":
			obj = [i for i in obj if i.city.name == city]


		

		form = MyRegistrationForm()
		profile = 1
		if request.user.is_authenticated:
			profile = Profile.objects.get(user = request.user)


		for i in obj:
			comments = Comment.objects.filter(obj = i)
			if len(comments) > 0:
				i.ratingDisplay = (i.rating // len(comments))
				i.ratingDisplay = round(i.ratingDisplay)


		return render(request, 'carsbg/results.html', {'results' : obj, "profile" : profile, "form" : form})

	if request.is_ajax():

		term = request.GET.get('term', '')
		results = []
		
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
			suggestions_json['label'] = i.address
			suggestions_json['category'] = "Местоположение:"

			results.append(suggestions_json)
			data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'

	return HttpResponse(data, mimetype)


def objectCreate(request, comments, result, users, services):

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
	
	currentUserComment = 0
	commentsObj = 0
	userFlag = 0
	servicesObj = 0



	result.append(Object.objects.filter(name = name, tel = tel, address = address, city = City.objects.filter(name = city)[0], typeOfObject = typeOfObject)[0])
	
	servicesObj = (Service.objects.filter(obj = result[0]))
	try:
		currentUserComment = Comment.objects.filter(obj = result[0], user = Profile.objects.filter(user = User.objects.filter(username = user)[0])[0])
		userFlag = 1
	except IndexError:
		pass
	if userFlag:
		try:
			commentsObj = Comment.objects.filter(obj = result[0]).exclude(user = Profile.objects.filter(user = User.objects.filter(username = user)[0])[0])
		except IndexError:
			pass
	else:
		try:
			commentsObj = Comment.objects.filter(obj = result[0])
		except IndexError:
			pass

	# elif typeOfObject == "Автокъща":
	# 	result.append(Object.objects.filter(name = name, tel = tel, address = address, city = City.objects.filter(name = city).first(), typeOfObject = typeOfObject).first())
	# 	commentsObj = Comment.objects.filter(obj = result[0])
	if currentUserComment:
		for comment in currentUserComment:
			comments.append(comment)
	if commentsObj:
		for comment in commentsObj:
			comments.append(comment)
	for service in servicesObj:
		services.append(service)




def viewObject(request):

	services = []
	comments = []	
	result = list()
	rating = 0
	users = []
	alert = ''
	
	objectCreate(request, comments, result, users, services)
	if len(comments) > 0:
		rating = result[0].rating // len(comments)
		rating = round(rating)

	form = MyRegistrationForm()
	profile = 1
	if request.user.is_authenticated:
		profile = Profile.objects.get(user = request.user)
	return render(request, 'carsbg/object.html', {'obj' : result[0], 'comments' : comments, "rating" : rating, 'alert' : alert, "form" : form, "profile" : profile, "services" : services})


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

			commentObj = Comment(text = comment, user = Profile.objects.filter(user = User.objects.filter(username = user)[0])[0], obj = obj, ip = ip, date = timezone.now().date(), rate = str(rating))
			commentObj.save()



		result = Object.objects.get(pk = pk, typeOfObject = typeOfObject)
		comments = Comment.objects.filter(obj = result)
		print(result)
		if limitExceeded == 0:
			result.rating = result.rating + rating
			result.save()

		if len(comments) > 0:
			rating = result.rating // len(comments)

	
	return JsonResponse({"alert" : alert}, safe = False)

def deleteComment(request):
	user = request.GET.get('user')
	pk = request.GET.get('pk')

	comment = Comment.objects.get(obj = Object.objects.get(pk = pk), user = Profile.objects.filter(user = User.objects.filter(username = user)[0])[0])
	obj = Object.objects.get(pk = pk)
	obj.rating -= int(comment.rate)

	if obj.rating < 0:
		obj.rating = 0

	obj.save()
	comment.delete()
	return JsonResponse("Success", safe = False)


def displayService(request, pk):
	service = Service.objects.get(pk = pk)

	form = MyRegistrationForm()
	profile = 1
	if request.user.is_authenticated:
		profile = Profile.objects.get(user = request.user)
	return render(request, "carsbg/servicePage.html", {"service" : service, "form" : form, "profile" : profile})