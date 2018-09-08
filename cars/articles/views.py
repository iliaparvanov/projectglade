from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.utils import timezone
from .forms import *


def articlePage(request):
	form = MyRegistrationForm()

	return render(request, 'articles/addArticle.html', {"form" : form})

def addArticle(request):
	if request.POST:
		nameOfArticle = request.POST.get('name', '')
		text = request.POST.get('text', '')
		user = request.POST.get('user', '')
		img = request.FILES.get('img', False)
		author =  User.objects.filter(username = user)[0]
		date = timezone.now().date()

		article = Article(name = nameOfArticle, text = text, image = img, author = author, date = date)
		article.save()
		alert = "Статията е запазена"
		
		return redirect('displayArticles')
	

def displayArticles(request):
	articles = Article.objects.all()
	form = MyRegistrationForm()

	return render(request, 'articles/displayArticles.html', {"articles" : articles, "form" : form})

@csrf_exempt
def articleText(request):
	if request.POST:
		name = request.POST.get('name', '')
		author = User.objects.get(username = request.POST.get('author'))

		article = Article.objects.get(name = name, author = author)

		return render(request, 'articles/articleText.html', {"article" : article})
