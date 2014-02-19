from django import forms
from django.forms import ModelForm
from pickupApp.constants import sport_choices, location_choices, num_choices
import datetime

class RegisterForm(forms.Form):
	first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
	email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))
	password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
	password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))

	def clean_password2(self):
		# Check that the two password entries match
		password = self.cleaned_data.get("password")
		password2 = self.cleaned_data.get("password2")
		if password and password2 and password != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

class LoginForm(forms.Form):
	email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))
	password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))

class GameForm(forms.Form):
	sport = forms.ChoiceField(sport_choices, widget=forms.Select(attrs={'class':'form-control', 'placeholder':'Basketball'}))
	name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Game Name'}))
	location = forms.ChoiceField(location_choices, widget=forms.Select(attrs={'class':'form-control', 'placeholder':'Location'}))
	cap = forms.ChoiceField(num_choices, widget=forms.Select(attrs={'class':'form-control', 'placeholder':'Number of Players'}))
	#description = forms.CharField(max_length=400, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Description'}))
	#timeStart = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class':'form-control', 'placeholder':'Game Time'}),initial=datetime.datetime.now())


# Need form to search and filter, then automatically populate lat/lon
# Additionally Need user to be able to add a new location name
# class GameLocationForm(forms.Form):

