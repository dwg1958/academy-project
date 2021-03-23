
from django.contrib.auth.models import User
from django import forms
from .models import Profile

## Email Form ####################
class EmailPostForm(forms.Form):
    subject  = forms.CharField(max_length=25)
    to       = forms.EmailField()
    message  = forms.CharField(required=True, widget=forms.Textarea)

## Login Form ####################
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

## Registration Form #############
class UserRegistrationForm(forms.ModelForm):
    password  = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','email')
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


## User Record Edit Form ############
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

## User Profile Form ################
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo', 'opt_in_to_email')
