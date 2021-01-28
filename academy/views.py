
from django.http import HttpResponse
from django.shortcuts import render


def homepage(request):
	return render(request, 'homepage.html', {'name':'David'})


def hithere(request):
	return HttpResponse('Hello')