from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.utils import timezone

def articlePage(request):
    return render(request, 'articles/addArticle.html')

def addArticle(request):
	if request.POST:
		nameOfArticle = request.POST.get('name', '')
		text = request.POST.get('text', '')
		user = request.POST.get('user', '')
		print(nameOfArticle + "01230143")
		author =  User.objects.filter(username = user)[0]
		date = timezone.now().date()

		article = Article(name = nameOfArticle, text = text, author = author, date = date)
		article.save()
		alert = "Статията е запазена"
		
		return redirect('displayArticles')
	

def displayArticles(request):
	articles = Article.objects.all()
	return render(request, 'articles/displayArticles.html', {"articles" : articles})

@csrf_exempt
def articleText(request):
	if request.POST:
		name = request.POST.get('name', '')
		author = User.objects.get(username = request.POST.get('author'))

		article = Article.objects.get(name = name, author = author)

		return render(request, 'articles/articleText.html', {"article" : article})
