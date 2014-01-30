from django import forms
from django.forms import ModelForm

class RegisterForm(forms.Form):
	first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
	email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))
	password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))

class LoginForm(forms.Form):
	email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))
	password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))