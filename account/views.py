
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import EmailPostForm, LoginForm
from django.core.mail import send_mail

## ACCOUNT DASHBOARD ################################
@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

'''
## LOGIN ############################################
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    return render(request, 'account/login.html', {'form': form,'messagecolour':'red','message':"Sorry, Your account has been disabled -call us!"  })
            else:
                return render(request, 'account/login.html', {'form': form,'messagecolour':'red','message':"Sorry, I can't find that user and password.."  })
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form,'messagecolour':'green','message':"Welcome, let's get you logged in.."  })
'''

## LOGOUT ##############################################
def logout(request):
	if request.method == 'POST':
			auth.logout(request)
			return redirect('home')


## REGISTER ############################################
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

# EMAIL FORM ##########################################
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
