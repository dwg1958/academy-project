
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import EmailPostForm, LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.core.mail import send_mail
from .models import Profile
from season.models import TeamProfile
from django.contrib.auth.decorators import user_passes_test


## ACCOUNT DASHBOARD ################################
@login_required
def dashboard(request):
    #return render(request, 'account/dashboard.html', {'section': 'dashboard'})
    return redirect('teamview')

## LOGOUT ##############################################
@login_required
def logout(request):
	if request.method == 'POST':
			auth.logout(request)
			return redirect('home')


# EMAIL FORM ##########################################
@user_passes_test(lambda u:u.is_staff, login_url='login')
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


## REGISTRATION ###################################
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            #Create a team profile just to be ready..
            TeamProfile.objects.create(user_ID=new_user)
            # Now say hi
            return render(request,
                          'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})

## Edit User record and Profile ###########################
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('dashboard')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,'account/edit.html', {'user_form': user_form,'profile_form': profile_form})





















'''
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
'''
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
