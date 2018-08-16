from django.shortcuts import render

def carsCompare(request):
	return render(request, "carscompare/home.html")