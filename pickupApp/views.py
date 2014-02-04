from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from pickupApp.forms import RegisterForm, LoginForm, GameForm
from pickupApp.models import Game, Location
import datetime
import json
from django.http import HttpResponse
from pickupApp.constants import location_to_coordinates
from collections import defaultdict

# Create your views here.
def index(request):
	print request.user
	if request.user.is_authenticated():
		return redirect('/home')

	num_games = get_num_games()
	return render(request, 'index.html', {'num_games':num_games})

def get_num_games():
	num_games = defaultdict(lambda:0)
	all_games = Game.objects.all()
	for game in all_games: 
		num_games[game.sport] += 1

	return num_games

@login_required
def home(request):
	print request
	print request.user.first_name

	games_json = get_games()
	return render(request, 'home.html', {'user':request.user, 'games_json':games_json})

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			email = form.cleaned_data['email']	
			password = form.cleaned_data['password']
			
			if not User.objects.filter(username=email).count():
				# need an if here to check if passwords match
				new_user = User.objects.create_user(email, email, password)
				new_user.first_name = first_name
				new_user.last_name = last_name
				new_user.save()

				user = authenticate(username=email, password=password)
				login(request, user)

				#return render(request, 'home.html', {'user': user})
				return redirect('/home')
			else:
				print form.errors
				#return render(request, 'home.html', {'registerForm':form})
				return redirect('/')
		else:
			print "INVALID FORM"
			print form.errors
			return redirect('/')
	else:
		print "GET"
		first_name = form.cleaned_data['first_name']
		last_name = form.cleaned_data['last_name']
		form = RegisterForm()
		return redirect('/')

@login_required
def create_game(request):
	if request.method == 'POST':
		form = GameForm(request.POST)
		if form.is_valid():
			sport = form.cleaned_data['sport']
			name = form.cleaned_data['name']
			description = form.cleaned_data['description']
			timeStart = form.cleaned_data['timeStart']
			location_name = form.cleaned_data['location']
			location = Location.objects.get(name=location_name)

			newGame = Game.objects.create(sport=sport,name=name,description=description,timeStart=timeStart, creator=request.user, location=location)
			newGame.dateCreated = datetime.datetime.now()
			#(latitude, longitude) = parse_location(location_to_coordinates[location])
			# newGame.latitude = latitude
			# newGame.longitude = longitude
			#newGame.location = location
		
			newGame.save()
			return redirect('/home')
		else:
			return render(request, 'game.html', {'gameForm':form})
	else:
		gameForm = GameForm()
		return render(request, 'create_game.html', {'gameForm':gameForm})

def parse_location(location):
	coordinates = location.split(',')
	return (float(coordinates[0]),float(coordinates[1]))

def user_login(request):
	if request.method == 'POST': 
		print "POSTING"
		form = LoginForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']	
			password = form.cleaned_data['password']
			print email
			print "SUCCESS"

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

#@login_required
def get_games():
	all_games = Game.objects.all()
	games_data = {}
	for game in all_games:
		location = game.location.name
		
		if not location in games_data:
			info = {}
			games_info = []
			location_info = {}
			location_info['latitude'] = game.location.latitude
			location_info['longitude'] = game.location.longitude
			info['location_info'] = location_info
			info['games'] = games_info
			
			games_data[location] = info

		game_data = {}
		game_data['name'] = game.name
		game_data['creator'] = game.creator.first_name+' '+game.creator.last_name
		game_data['description'] = game.description
		#game_data['time_start'] = game.timeStart
		game_data['sport'] = game.sport
		#game_data['location'] = game.location

		games_data[location]['games'].append(game_data)
	return json.dumps(games_data)

	#return HttpResponse(json.dumps(games_data), content_type="application/json")


def logout_view(request):
	logout(request)
	return redirect("/")

def team(request):
	return render(request, 'team.html')

def game(request):
	return render(request, 'game.html')

def features(request):
	return render(request, 'features.html')

def base(request):
	return render(request, 'base.html')

def services(request):
	return render(request, 'services.html')

def home(request):
	
	return render(request, 'home.html')
