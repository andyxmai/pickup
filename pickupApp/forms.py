from django import forms
from django.forms import ModelForm
from pickupApp.constants import sport_choices, location_choices
import datetime

class RegisterForm(forms.Form):
	first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
	email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))
	password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))

class LoginForm(forms.Form):
	email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))
	password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))

class GameForm(forms.Form):
	sport = forms.ChoiceField(sport_choices, widget=forms.Select(attrs={'class':'form-control', 'placeholder':'Basketball'}))
	name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Game Name'}))
	location = forms.ChoiceField(location_choices, widget=forms.Select(attrs={'class':'form-control', 'placeholder':'Location'}))
	description = forms.CharField(max_length=400, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Description'}))
	timeStart = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Game Time'}),initial=datetime.datetime.now)
