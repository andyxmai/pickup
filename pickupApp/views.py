from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from pickupApp.forms import RegisterForm, LoginForm, GameForm
from pickupApp.models import Game
import datetime

# Create your views here.
def index(request):
	print 'index'
	return render(request, 'index.html')

@login_required
def home(request):
	return render(request, 'home.html', {'user':request.user})

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			email = form.cleaned_data['email']	
			password = form.cleaned_data['password']

			print first_name

			new_user = User.objects.create_user(email, email, password)
			new_user.first_name = first_name
			new_user.last_name = last_name
			new_user.save()

			user = authenticate(username=email, password=password)
			login(request, user)

			return redirect('/home')
	else:
		registerForm = RegisterForm()
		return render(request, 'register.html', {'registerForm':registerForm})
	# first_name = request.POST.get('first_name')
	# last_name = request.POST.get('last_name')
	# email = request.POST.get('email')
	# password = request.POST['password']

@login_required
def create_game(request):
	if request.method == 'POST':
		form = GameForm(request.POST)
		if form.is_valid():
			sport = form.cleaned_data['sport']
			name = form.cleaned_data['name']
			description = form.cleaned_data['description']
			timeStart = form.cleaned_data['timeStart']

			newGame = Game.objects.create(sport=sport,name=name,description=description,timeStart=timeStart, creator=request.user)
			newGame.dateCreated = datetime.datetime.now()
			#newGame.creator_of_game = request.user

			newGame.save()
			return redirect('/home')
		else:
			return render(request, 'game.html', {'gameForm':form})
	else:
		gameForm = GameForm()
		return render(request, 'game.html', {'gameForm':gameForm})

	

def user_login(request):
	if request.method == 'POST': 
		form = LoginForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']	
			password = form.cleaned_data['password']

			user = authenticate(username=email, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('/home')
				else:
					return render(request, 'login.html', {'loginForm':form})
			else:
				return render(request, 'login.html', {'loginForm':form})
		else:
			return render(request, 'login.html', {'loginForm':form})
	else:
		form = LoginForm()
		return render(request, 'login.html', {'loginForm':form})


def logout(request):
	logout(request)
	return redirect("/")
