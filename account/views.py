
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .forms import EmailPostForm
from django.core.mail import send_mail


# Create your views here.

def login(request):
    #print ('HERE')
    return render(request, 'account/login.html')

def logout(request):
	if request.method == 'POST':
			auth.logout(request)
			return redirect('home')


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

# EMAIL FORM #################
def email(request):#, post_id):
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            subject = f"{cd['subject']}"
            message = f"Message reads: {cd['message']}"
            sentOK = send_mail(subject, message, 'gp@gpgrandstand.com', [cd['to']])
    else:
        form    = EmailPostForm()
        subject = ""  #placeholder to allow render below before data received
        sentOK  = ""  #placeholder to allow render below before data received
    return render(request, 'account/email.html', {'form': form, 'subject':subject, 'sentOK':sentOK}) #{'post': post,'form': form})
