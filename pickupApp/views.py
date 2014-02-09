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
from pickupApp.constants import sports_dict
#import smtplib # For sending emails
#import datetime
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.messages import get_messages


# Create your views here.
def index(request):
	print request.user
	if request.user.is_authenticated():
		return redirect('/home')

	num_games = get_num_games()
	messages = get_messages(request)
	return render(request, 'index.html', {'num_games':num_games, 'messages':messages})

def get_num_games():
	num_games = defaultdict(lambda:0)
	all_games = Game.objects.all()
	for game in all_games: 
		num_games[game.sport] += 1

	return num_games

@login_required
def get_games(request):
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
		game_data['id'] = game.id
		game_data['name'] = game.name
		game_data['creator'] = game.creator.first_name+' '+game.creator.last_name
		game_data['description'] = game.description
		#game_data['time_start'] = game.timeStart
		game_data['sport'] = game.sport
		game_data['curr_num_players'] = game.users.count()+1
		game_data['max_num_players'] = game.cap
		#game_data['location'] = game.location

		games_data[location]['games'].append(game_data)
	return games_data
	#return HttpResponse(json.dumps(games_data), content_type="application/json")

@login_required
def home(request):

	games_data = get_games(request)
	#print games_data
	messages = get_messages(request)
	return render(request, 'home.html', {'user':request.user, 'games_json':json.dumps(games_data), 'messages':messages})

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
			cap = form.cleaned_data['cap']
			location_name = form.cleaned_data['location']
			location = Location.objects.get(name=location_name)

			#Need to handle time zones
			datetimeStart = request.POST['dtp_input1']
			
			newGame = Game.objects.create(sport=sport,name=name,timeStart=datetimeStart, creator=request.user, location=location, cap=cap)
			newGame.dateCreated = datetime.datetime.now()
	
			newGame.save()
			return redirect('/game/'+str(newGame.id))
		else:
			print 'invalid form'
			error_msg = 'Could not create your game. Please try again!'
			return render(request, 'create_game.html', {'gameForm':form, 'error_msg':error_msg})
	else:
		gameForm = GameForm()
		return render(request, 'create_game.html', {'gameForm':gameForm})

def parse_location(location):
	coordinates = location.split(',')
	return (float(coordinates[0]),float(coordinates[1]))

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
					return render(request, 'in.html', {'loginForm':form})
			else:
				msg = 'Invalid username and password.'
				messages.success(request, msg)
				return redirect('/')
				#return render(request, 'login.html', {'loginForm':form, 'message':message})
		else:
			msg = 'Invalid username and password.'
			messages.success(request, msg)
			return redirect('/')
			#return render(request, 'login.html', {'loginForm':form, 'message':message})
	else:
		return redirect('/')
		#form = LoginForm()
		#return render(request, 'login.html', {'loginForm':form})

@login_required
def game(request,id):
	game = Game.objects.get(id=id)

	is_creator = False
	if request.user == game.creator:
		is_creator = True

	joined = False
	if request.user in game.users.all() or is_creator:
		joined = True
	return render(request, 'game.html', {'game':game, 'joined':joined, 'is_creator':is_creator, 'user':request.user})

@login_required
def join_quit_game(request):
	#userID = request.user.id
	response = ''
	if request.method == 'POST': 
		game_id = request.POST['game_id']
		print game_id
		
		game = Game.objects.get(id=game_id)
		if request.user in game.users.all():
			game.users.remove(request.user)
			response = 'left'
		else:
			game.users.add(request.user)
			response = 'joined'
	
	#return HttpResponse(response)
	return redirect('/game/'+game_id)

def send_an_email(receivers,subj,msg):
	# sender = "ReqTime <debugsafedriven@gmail.com>"
	# server = smtplib.SMTP('smtp.gmail.com',587)
	# username = 'debugsafedriven'
	# password = 'fratpad2014'
	# server.starttls()
	# server.ehlo()
	# server.login(username,password)
	# date = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )
	# fullMsg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % (sender, receivers, subj, date, msg )
	# print receivers
	# server.sendmail(sender,receivers,fullMsg)
	# server.quit()

	sender = "ReqTime <debugsafedriven@gmail.com>"
	send_mail(subj, msg, sender, receivers, fail_silently=False)

@login_required
def delete_game(request):
	if request.method == 'POST':
		game_id = request.POST['game_id']
		g = Game.objects.get(id=game_id)

		receivers = []
		allUsers = g.users.all()
		if len(allUsers) != 0:
			for user in g.users.all():
				print user
				receivers.append(user.username)

			game_maker = "%s %s" % (g.creator.first_name, g.creator.last_name)
			msg = "Unfortunately, %s has cancelled %s." % (game_maker, g.name)
			subj = "%s Game Cancellation" % (g.name)
			send_an_email(receivers,subj,msg)

		msg = g.name + ' (' + g.sport + ')' + ' was deleted.'
		g.delete()
		messages.success(request, msg)

	return redirect('/home')

def logout_view(request):
	logout(request)
	return redirect("/")

def team(request):
	return render(request, 'team.html')

def services(request):
	return render(request, 'services.html')

def about(request):
	return render(request, 'about.html')

@login_required
def sport(request, sport):
	sport = sport.lower()
	if sport in sports_dict:
		games_with_sport = Game.objects.filter(sport=sport)
		sport = sports_dict[sport]
		return render(request, 'sport.html', {'games_with_sport':games_with_sport, 'sport':sport})
	else:
		return redirect('/')

def user(request, id):
	user = User.objects.get(pk=id)
	games_created = Game.objects.filter(creator=user)
	games_played = user.game_set.all().order_by('-timeStart');
	upcoming_games = user.game_set.all().filter(timeStart__gte=datetime.datetime.now()).order_by('-timeStart');
	return render(request, 'user.html', {'user':user, 'games_played':games_played, 'games_created':games_created, 'upcoming_games': upcoming_games})
