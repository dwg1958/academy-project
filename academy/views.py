
from django.http import HttpResponse
from django.shortcuts import render


def homepage(request):
	return render(request, 'homepage.html', {'yourname':'David'})

def aboutpage(request):
	textreceived = request.GET['fname']
	return render(request, 'about.html', {'name': textreceived})


def hithere(request):
	return HttpResponse('Hello')
