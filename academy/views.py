
#from django.http import HttpResponse
from season.models import Parameter, TeamProfile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth

def homepage(request):
	front_page_news     =  get_object_or_404(Parameter, name = 'front_page_news').long_text
	front_page_unsigned =  get_object_or_404(Parameter, name = 'front_page_unsigned').long_text
	try:
		teamname    =  get_object_or_404(TeamProfile, pk=request.user.team.id).teamName
	except:
		teamname = " "
	return render(request, 'homepage.html', {'section': 'home', 'front_page_news':front_page_news, 'front_page_unsigned':front_page_unsigned, 'teamname':teamname})

def aboutpage(request):
	#textreceived = request.GET['fname']
	return render(request, 'about.html')#, {'name': textreceived})
'''
def register(request):
	if request.method == 'POST':
		#register data received
		if request.POST['password1'] == request.POST['password2']:
			try:
				user = User.objects.get(username = request.POST['username'])
				return render(request, 'season/maketeam.html', {'message': 'Username already taken'})
			except User.DoesNotExist:
				user = User.objects.create_user( request.POST['username'], request.POST['email'], password=request.POST['password1'])
				user.last_name = request.POST['lastname']
				user.first_name = request.POST['firstname']
				user.save()
				auth.login(request,user)
				return redirect('home') #,{'message': 'You are registered and logged in'} )
		else:
			return render(request, 'season/maketeam.html', {'message': 'Passwords must match, Doofus'})
	else:
		#show blank form
		return render(request, 'season/maketeam.html')
'''
'''
def login(request):
	#register data received
	if request.method == 'POST':
		user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None:
			auth.login(request, user)
			return redirect('home')
		else:
			return render(request, 'login.html', {'message':"Sorry, I can't find that user and password.."  })
	else:
		return render(request, 'login.html')
'''
'''
def logout(request):
	if request.method == 'POST':
			auth.logout(request)
			return redirect('home')
'''

# Reset password################################
'''
>>> from django.contrib.auth.models import User
>>> u = User.objects.get(username='john')
>>> u.set_password('new password')
>>> u.save()
'''

# def hithere(request):
#	return HttpResponse('Hello')
