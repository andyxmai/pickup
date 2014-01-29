from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
	print 'index'
	return render(request, 'index.html')

@login_required
def home(request):
	return render(request, 'home.html', {'user':request.user})

def register(request):
	# first_name = request.POST.get('first_name')
	# last_name = request.POST.get('last_name')
	# email = request.POST.get('email')
	# password = request.POST['password']
	return render(request, 'register.html', {'user':request.user})

	print password

	new_user = User.objects.create_user(email, email, password)
	new_user.first_name = first_name
	new_user.last_name = last_name
	new_user.save()

	user = authenticate(username=email, password=password)
	login(request, user)

	return redirect('/home')

def user_login(request):
	email = request.POST.get('email')
	password = request.POST.get('password')

	user = authenticate(username=email, password=password)
	if user is not None:
		if user.is_active:
			login(request, user)
			return redirect('/home')
		else:
			return redirect('/')
	else:
		return redirect('/')