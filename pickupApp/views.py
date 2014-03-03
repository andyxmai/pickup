from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from pickupApp.forms import RegisterForm, LoginForm, GameForm, CommentForm
from pickupApp.models import Game, Location, Comment, InstagramInfo, GamePhoto, UserInfo
import datetime
import json, ast
from django.http import HttpResponse
from pickupApp.constants import location_to_coordinates
from collections import defaultdict
from pickupApp.constants import sports_dict
#import smtplib # For sending emails
#import datetime
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.messages import get_messages
from notifications import notify
from django.db.models import Q
from pickup.settings import INSTAGRAM_ID, INSTAGRAM_SECRET, REDIRECT_URL, FACEBOOK_APP_ID, FACEBOOK_URL
import urllib2, urllib
from instagram.client import InstagramAPI

# For Django Activity Stream
from django.db.models.signals import post_save
from actstream import action 
from actstream.models import Action, user_stream, actor_stream, action_object_stream, model_stream, following, followers
from actstream.actions import follow,unfollow

from django.core import serializers

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
	upcoming_games = Game.objects.filter(timeStart__gte=datetime.datetime.now()).order_by('timeStart');
	games_data = {}
	for game in upcoming_games:
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
		game_data['curr_num_players'] = game.users.count()
		game_data['max_num_players'] = game.cap
		#game_data['location'] = game.location

		games_data[location]['games'].append(game_data)
	return games_data
	#return HttpResponse(json.dumps(games_data), content_type="application/json")



# {"pk": 12, 
# "model": "actstream.action", 
# "fields": {
# 	"action_object_object_id": null, 
# 	"description": null, 
# 	"timestamp": "2014-03-02T00:24:34.843Z", 
# 	"action_object_content_type": null, 
# 	"actor_object_id": "1", 
# 	"verb": "started following", 
# 	"target_object_id": "2", 
# 	"actor_content_type": 4, 
# 	"data": null, 
# 	"public": true, 
# 	"target_content_type": 4
# 	}
# }
@login_required
def home(request):
	#Group.objects.create(name="All Users")
	games_data = get_games(request)
	#print games_data
	print "In home"

	#print Action.objects.all()
	print user_stream(request.user)
	mystream = user_stream(request.user)
	#stream = actor_stream(request.user)
	

	#for action in stream:
		#print json.stringify(action)
		# print action
		# print action.verb
		# print action.actor
		# print action.action_object
		# print action.timestamp.strftime('%Y')
		#data = serializers.serialize("json", Action.objects.all())
		#print data

	all_actions = mystream.filter(timestamp__lt=datetime.datetime.now()).order_by('timestamp');
	print "Printing all_actions"
	print all_actions

	following_people = following(request.user)
	print "People I am following"
	print following_people
	if not len(following_people):
		all_actions = []

	messages = get_messages(request)
	unread = request.user.notifications.unread()
	for note in unread:
		print note.ValueErrorrb
	return render(request, 'home.html', {
		'user':request.user, 
		'games_json':json.dumps(games_data), 
		'messages': messages,
		'actions' : all_actions
		})

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
				new_user.groups = "All Users"
				new_user.save()

				user = authenticate(username=email, password=password)
				login(request, user)
				verb = first_name + ' ' + last_name + " created an account!"
				print verb
				#action.send(user,verb=verb)


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
			newGame.users.add(request.user)
	
			newGame.save()
			action.send(request.user,verb="game created",action_object=newGame)
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
				messages.error(request, msg)
				return redirect('/')
				#return render(request, 'login.html', {'loginForm':form, 'message':message})
		else:
			msg = 'Invalid username and password.'
			messages.error(request, msg)
			return redirect('/')
			#return render(request, 'login.html', {'loginForm':form, 'message':message})
	else:
		return redirect('/')
		#form = LoginForm()
		#return render(request, 'login.html', {'loginForm':form})

@login_required
def game(request,id):
	game_exists = Game.objects.filter(id=id).count()
	if game_exists:
		game = Game.objects.get(id=id)
		print action_object_stream(game)

		# try:
		# 	action_object_stream(game)
		# except ValueError:
		# 	print ValueError
		comment_form = CommentForm(initial={'user_id': request.user.id, 'game_id':game.id})
		# Check whether the game has already happened
		if game.timeStart.replace(tzinfo=None) < datetime.datetime.now():
			passed_game = True
		else:
			passed_game = False

		# Check if the game player has maxed
		maxed = False
		if game.users.count() >= game.cap:
			maxed = True	

		# Check if user is the creator of the game
		is_creator = False
		if request.user == game.creator:
			is_creator = True

		# Check if user has joined the game
		joined = False
		if request.user in game.users.all() or is_creator:
			joined = True

		connected_to_instagram = False
		if InstagramInfo.objects.filter(user=request.user).count():
			connected_to_instagram = True

		return render(request, 'game.html', {
			'game':game, 
			'joined':joined, 
			'is_creator':is_creator, 
			'user':request.user, 
			'game_exists':game_exists, 
			'passed_game':passed_game, 
			'maxed':maxed, 
			'comment_form':comment_form, 
			'connected_to_instagram':connected_to_instagram
		})
	else:
		return render(request, 'game.html', {'game_exists':game_exists})
	



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
			verb = request.user.first_name+' '+request.user.last_name+' left '+game.name
			notify.send(request.user,recipient=game.creator, verb=verb)
			action.send(request.user, verb="leave game", action_object=game)
		else:
			game.users.add(request.user)
			response = 'joined'
			verb = request.user.first_name+' '+request.user.last_name+' joined '+game.name
			notify.send(request.user,recipient=game.creator, verb=verb)
			action.send(request.user, verb="join game", action_object=game)
	
	#return HttpResponse(response)
	return redirect(request.META['HTTP_REFERER'])

def send_an_email(receivers,subj,msg):
	sender = "ReqTime <debugsafedriven@gmail.com>"
	send_mail(subj, msg, sender, receivers, fail_silently=False)

@login_required
def delete_game(request):
	if request.method == 'POST':
		game_id = request.POST['game_id']
		g = Game.objects.get(id=game_id)
		verb = request.user.first_name+' '+request.user.last_name+' cancelled '+g.name;
		action.send(request.user,verb=verb,action_object=g)
		receivers = []
		allUsers = g.users.all()
		if len(allUsers) != 0:
			for user in g.users.all():
				print user
				receivers.append(user.username)
				verb = request.user.first_name+' '+request.user.last_name+' cancelled '+g.name
				notify.send(request.user,recipient=user, verb=verb)

			game_maker = "%s %s" % (g.creator.first_name, g.creator.last_name)
			msg = "Unfortunately, %s has cancelled %s." % (game_maker, g.name)
			subj = "%s Game Cancellation" % (g.name)
			# send_an_email(receivers,subj,msg)

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

#@login_required
def sport(request, sport):
	sport = sport.lower()
	authenticated = False
	if sport in sports_dict:
		if request.user.is_authenticated():
			authenticated = True
		games_with_sport = Game.objects.filter(sport=sport)
		sport = sports_dict[sport]
		return render(request, 'sport.html', {'games_with_sport':games_with_sport, 'sport':sport, 'authenticated':authenticated})
	else:
		return redirect('/')

@login_required
def user(request, id):
	loggedinUser = request.user
	player = User.objects.get(pk=id)
	if player == loggedinUser:
		return redirect('/profile')

	print user_stream(request.user)

	games_created = Game.objects.filter(creator=player)
	games_played = player.game_set.all().filter(timeStart__lt=datetime.datetime.now()).order_by('-timeStart');
	upcoming_games = player.game_set.all().filter(timeStart__gte=datetime.datetime.now()).order_by('timeStart');

	player_connected_to_instagram = False
	if InstagramInfo.objects.filter(user=player).count():
		player_connected_to_instagram = True

	following_people = following(request.user)
	is_following = player in following_people

	return render(request, 'user.html', {
		'player':player, 
		'games_played':games_played, 
		'games_created':games_created, 
		'upcoming_games': upcoming_games, 
		'loggedinUser':loggedinUser,
		'player_connected_to_instagram': player_connected_to_instagram,
		'is_following' : is_following
		})
	
@login_required
def remove_notifications(request):
	request.user.notifications.mark_all_as_read()
	return HttpResponse('')

def search_game(request):
	if not 'id' in request.session:
		return redirect('/')

	if request.is_ajax():
	    q = request.GET['query']
	    results = []
	    games = Game.objects.filter(name__icontains = q )[:6]
	    for game in games:
				game_json = {}
				game_json['id'] = game.id
				game_json['name'] = game.name
				game_json['type'] = 'game'
				results.append(game_json)
	    data = json.dumps(results)
	else:
	    data = 'fail'
	
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)

def search_people(request):
	if not 'id' in request.session:
		return redirect('/')

	if request.is_ajax():
	    q = request.GET['query']
	    results = []
	    users = User.objects.filter(name__icontains = q )[:6]
	    for user in users:
				user_json = {}
				user_json['id'] = user.id
				user_json['name'] = user.first_name + ' ' + user.last_name
 				user_json['type'] = 'user'
				results.append(user_json)
	    data = json.dumps(results)
	else:
	    data = 'fail'
	
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)

@login_required
def profile(request):
	loggedinUser = request.user
	user = request.user
	games_created = Game.objects.filter(creator=user)
	games_played = Game.objects.filter(timeStart__lt=datetime.datetime.now()).order_by('-timeStart');
	upcoming_games = user.game_set.all().filter(timeStart__gte=datetime.datetime.now()).order_by('timeStart');
	
	connected_to_instagram = False
	if InstagramInfo.objects.filter(user=user).count():
		connected_to_instagram = True

	print FACEBOOK_URL

	return render(request, 'user.html', 
		{'player':user, 
		'games_played':games_played, 
		'games_created':games_created, 
		'upcoming_games': upcoming_games, 
		'loggedinUser':loggedinUser,
		'instagramID' : INSTAGRAM_ID,
		'instagramSecret' : INSTAGRAM_SECRET,
		'redirectURL' : REDIRECT_URL,
		'connected_to_instagram': connected_to_instagram,
		'facebookID' : FACEBOOK_APP_ID,
		'websiteURL' : FACEBOOK_URL,
		'following' : following(request.user)
		})

def sports(request):
	return render(request, 'sports.html', {'sports_dict':sports_dict})

def search(request):
	q = request.GET['term']
	results = []
	users = User.objects.filter(Q(first_name__icontains = q)|Q(last_name__icontains = q))[:6]
	print users
	if users:
		print 'theres users for '+q
		for user in users:
			user_json = {}
			user_json['id'] = user.id
			user_json['value'] = user.first_name + ' ' + user.last_name
			user_json['label'] = user.first_name + ' ' + user.last_name
			user_json['category'] = 'People'
			results.append(user_json)

	games = Game.objects.filter(name__icontains = q )[:6]
	if games:
		for game in games:
			game_json = {}
			game_json['id'] = game.id
			game_json['value'] = game.name
			game_json['label'] = game.name
			game_json['category'] = 'Games'
			results.append(game_json)

	mimetype = 'application/json'
	return HttpResponse(json.dumps(results), mimetype)

@login_required
def comment(request):
	if request.method == 'POST':
		#store comment
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid():
			text = comment_form.cleaned_data['text']
			user_id = comment_form.cleaned_data['user_id']
			game_id = comment_form.cleaned_data['game_id']

			commenter = User.objects.get(id=user_id)
			game = Game.objects.get(id=game_id)
			comment = Comment.objects.create(text=text, commenter=commenter, game=game, timeStamp=datetime.datetime.now())

			for player in game.users.all():
				if commenter != player:
					verb = commenter.first_name+' '+commenter.last_name+' left a comment for '+game.name
					notify.send(commenter,recipient=player, verb=verb)

			return redirect('/game/'+str(game.id))
		else:
			return redirect('/')
	else:
		return redirect('/')

@login_required
def instagram_login(request):
	code = request.GET['code']
	print "Code = "
	print code
	paramsDict = {
		'client_id' : INSTAGRAM_ID,
		'client_secret' : INSTAGRAM_SECRET,
		'grant_type' : 'authorization_code',
		'redirect_uri' : REDIRECT_URL,
		'code' : code
	}
	print "Params = "
	params = urllib.urlencode(paramsDict);
	print params
	url = 'https://api.instagram.com/oauth/access_token'
	req = urllib2.Request(url,params)
	#f = urllib2.urlopen(req)
	opener = urllib2.build_opener()
	f = opener.open(req)
	instagram_data = json.load(f)

	newInstagram = InstagramInfo()
	newInstagram.access_token = instagram_data['access_token']
	newInstagram.username = instagram_data['user']['username']
	newInstagram.profile_picture = instagram_data['user']['profile_picture']
	newInstagram.full_name = instagram_data['user']['full_name']
	newInstagram.instagramID = instagram_data['user']['id']

	print newInstagram.full_name
	newInstagram.user = request.user
	newInstagram.save()

	return redirect('/profile')

@login_required
def get_instagram_photos(request, game_id):
	instagramUser = InstagramInfo.objects.get(user=request.user)
	access_token = instagramUser.access_token
	api = InstagramAPI(access_token=access_token)
	recent_media, next = api.user_recent_media(count=5)
	instagram_photos = []
	for media in recent_media:
		photo = {}
		photo['thumbnail'] = media.images['thumbnail'].url
		photo['standard'] = media.images['standard_resolution'].url
		instagram_photos.append(photo)
	
	return render(request, 'get_instagram_photos.html', {
		'instagram_photos':instagram_photos, 
		'game_id':game_id
	})
	
@login_required
def post_photos(request):
	if request.method == 'POST':
		game_photos = None
		game = Game.objects.get(id=request.POST['game_id'])
		if 'photos' in request.POST:
			game_photos = request.POST.getlist('photos')

		if game_photos:
			for photo in game_photos:
				photo_dict = ast.literal_eval(photo)
				if not GamePhoto.objects.filter(thumbnail=photo_dict['thumbnail']).exists():
					game_photo = GamePhoto.objects.create(thumbnail=photo_dict['thumbnail'], standard=photo_dict['standard'], game=game)
					action.send(request.user,verb="photo upload",action_object=game_photo)

	return redirect('/game/'+str(game.id)) 

@login_required
def upload_profile_photo(request):
	if request.method == 'POST':
		photo_url = request.POST['photo_url']
		user_info = UserInfo.objects.get(user=request.user)
		user_info.profile_picture = photo_url
		user_info.save()
		action.send(request.user,verb="profile photo",action_object=user_info)

	return redirect('/profile')

@login_required
def toggle_follow(request):
	if request.method == 'POST':
		following_people= following(request.user)
		follow_username = request.POST['player']

		# is_following = False
		# for user in following_people:
		# 	if user.username == follow_username:
		# 		is_following = True
		is_following = follow_username in following_people

		user = User.objects.get(username=follow_username)
		if not is_following:
			follow(request.user, user)
		else:
			unfollow(request.user, user)

		#responseData = {}
		response = ""
		if is_following:
			#responseData['follow'] = "No"
			response = "No"
		else:
			#responseData['follow'] = "Yes"
			response = "Yes"

	# return HttpResponse(json.dumps(responseData),mimetype="application/json")
	return HttpResponse(response)


@login_required
def analytics(request):
	# Player Analytics
	games_played = request.user.game_set.all()
	fav_sports = defaultdict(lambda:0)
	for game_played in games_played:
		fav_sports[game_played.sport] += 1
	fav_sports = sorted(fav_sports.iteritems(),key=lambda (k,v): v,reverse=True)

	# Sport Analytics
	freq_places = {}
	all_games = Game.objects.all()
	user = request.user
	for game in all_games:
		if game.sport in freq_places:
			freq_places[game.sport][game.location.name] += 1
		else:
			sport_loc = defaultdict(lambda:0)
			sport_loc[game.location.name] += 1
			freq_places[game.sport] = sport_loc

	sorted_freq_places = {}
	for k,places in freq_places.iteritems():
		sorted_places = sorted(places.iteritems(),key=lambda (k,v): v,reverse=True)
		sorted_freq_places[k] = sorted_places

	# Game Analytics
	all_games_played = Game.objects.filter(timeStart__lt=datetime.datetime.now()).order_by('-timeStart');
	games_played_breakdown = {}
	for game in all_games_played:
		if game.sport in games_played_breakdown:
			games_played_breakdown[game.sport] += 1
		else:
			games_played_breakdown[game.sport] = 1
	print games_played_breakdown

	return render(request, 'analytics.html', {
		'user' : user,
		'games_played'				: games_played,
		'fav_sports'				: fav_sports,
		'sorted_freq_places'		: sorted_freq_places,
		'all_games_played'			: all_games_played,
		'games_played_breakdown'	: games_played_breakdown
	})

@login_required
def first_login(request):
	return render(request, 'first_login.html', {'user':request.user})










