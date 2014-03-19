from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from pickupApp.forms import RegisterForm, LoginForm, GameForm, CommentForm
from pickupApp.models import Game, Location, Comment, InstagramInfo, GamePhoto, UserInfo, Sport, UserSportLevel
import datetime
import json, ast
from django.http import HttpResponse
from pickupApp.constants import location_to_coordinates
from collections import defaultdict
from pickupApp.constants import sports_dict
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
import math, operator



# -------------------------------------------------------------------- #
# Renders the landing page
# -------------------------------------------------------------------- #
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
		num_games[game.sport.name] += 1

	return num_games

# -------------------------------------------------------------------- #
# Gets all game data and puts it in a specific format we use later (json)
# -------------------------------------------------------------------- #
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
		game_data['sport'] = game.sport.name
		game_data['curr_num_players'] = game.users.count()
		game_data['max_num_players'] = game.cap
		#game_data['location'] = game.location

		games_data[location]['games'].append(game_data)
	return games_data
	#return HttpResponse(json.dumps(games_data), content_type="application/json")


# -------------------------------------------------------------------- #
# Function is called when home page is rendered
# Gives the home page the necessary data to render
# -------------------------------------------------------------------- #
@login_required
def home(request):
	games_data = get_games(request)
	mystream = user_stream(request.user)
	all_actions = mystream.filter(timestamp__lt=datetime.datetime.now()).order_by('-timestamp');
	following_people = following(request.user)
	if not len(following_people):
		all_actions = []
	messages = get_messages(request)
	
	# unread = request.user.notifications.unread()
	# for note in unread:
	# 	print note.verb

	game_recommendations = []
	if request.user.userinfo.latitude != None:
		game_recommendations = get_game_recommendations(request)

	return render(request, 'home.html', {
		'user'					:request.user, 
		'games_json'			:json.dumps(games_data), 
		'messages'				:messages,
		'actions' 				:all_actions,
		'game_recommendations' 	:game_recommendations
		})


# -------------------------------------------------------------------- #
# Registering a new user
# -------------------------------------------------------------------- #
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

				userinfo = UserInfo.objects.create(user=new_user)

				user = authenticate(username=email, password=password)
				login(request, user)
				verb = first_name + ' ' + last_name + " created an account!"

				#action.send(user,verb=verb)
				return redirect('/first_login')
				
			else:
				print form.errors
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


# -------------------------------------------------------------------- #
# Creating a new game
# -------------------------------------------------------------------- #
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

			sportObj = Sport.objects.get(name=sport.lower())
			newGame = Game.objects.create(sport=sportObj,name=name,timeStart=datetimeStart, creator=request.user, location=location, cap=cap)
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


# -------------------------------------------------------------------- #
# Logs the user in or redirects of bad login
# -------------------------------------------------------------------- #
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
		else:
			msg = 'Invalid username and password.'
			messages.error(request, msg)
			return redirect('/')
	else:
		return redirect('/')


# -------------------------------------------------------------------- #
# Function is called whenever a game page is rendered
# Function gets all the necessary data to populate the game page
# -------------------------------------------------------------------- #
@login_required
def game(request,id):
	game_exists = Game.objects.filter(id=id).count()
	if game_exists:
		game = Game.objects.get(id=id)
		print action_object_stream(game)

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
			'connected_to_instagram':connected_to_instagram,
			'instagramID' : INSTAGRAM_ID,
			'instagramSecret' : INSTAGRAM_SECRET,
			'redirectURL' : REDIRECT_URL,
		})
	else:
		return render(request, 'game.html', {'game_exists':game_exists})
	
# -------------------------------------------------------------------- #
# Function is called when a user wants to quit or join a game
# -------------------------------------------------------------------- #
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
			description = '/game/'+str(game.id)
			notify.send(request.user,recipient=game.creator, verb=verb, description=description)
			action.send(request.user, verb="leave game", action_object=game)
		else:
			game.users.add(request.user)
			response = 'joined'
			verb = request.user.first_name+' '+request.user.last_name+' joined '+game.name
			description = '/game/'+str(game.id)
			notify.send(request.user,recipient=game.creator, verb=verb, description=description)
			action.send(request.user, verb="join game", action_object=game)
	
	#return HttpResponse(response)
	return redirect(request.META['HTTP_REFERER'])


# -------------------------------------------------------------------- #
# Function deletes a game and sends an email to all members of the game
# -------------------------------------------------------------------- #
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
				notify.send(request.user,recipient=user, verb=verb, description='#')

			game_maker = "%s %s" % (g.creator.first_name, g.creator.last_name)
			msg = "Unfortunately, %s has cancelled %s." % (game_maker, g.name)
			subj = "%s Game Cancellation" % (g.name)
			#send_an_email(receivers,subj,msg)

		msg = g.name + ' (' + g.sport.name + ')' + ' was deleted.'
		g.delete()
		messages.success(request, msg)

	return redirect('/home')

def send_an_email(receivers,subj,msg):
	sender = "ReqTime <debugsafedriven@gmail.com>"
	send_mail(subj, msg, sender, receivers, fail_silently=False)


# -------------------------------------------------------------------- #
# Function is called when the user logouts
# -------------------------------------------------------------------- #
def logout_view(request):
	logout(request)
	return redirect("/")

# -------------------------------------------------------------------- #
# Function returns a static development team page
# -------------------------------------------------------------------- #
def team(request):
	return render(request, 'team.html')

# -------------------------------------------------------------------- #
# Function returns a static about team page
# -------------------------------------------------------------------- #
def about(request):
	return render(request, 'about.html')

# -------------------------------------------------------------------- #
# Function is deprecated
# -------------------------------------------------------------------- #
#@login_required
def sport(request, sport):
	sport = sport.lower()
	authenticated = False
	sport_obj = Sport.objects.get(name = sport)
	if sport_obj:
		if request.user.is_authenticated():
			authenticated = True
		#sport_obj = sport_set[0]
		games_with_sport = Game.objects.filter(sport=sport_obj)
		return render(request, 'sport.html', {'games_with_sport':games_with_sport, 'sport':sport, 'authenticated':authenticated})
	else:
		return redirect('/')

# -------------------------------------------------------------------- #
# Function is called when the user accesses a players profile page
# -------------------------------------------------------------------- #
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

# -------------------------------------------------------------------- #
# Removes all notifications of a user
# -------------------------------------------------------------------- #
@login_required
def remove_notifications(request):
	request.user.notifications.mark_all_as_read()
	return HttpResponse('')

# -------------------------------------------------------------------- #
# Function is called when the user accesses his/her own profile page
# -------------------------------------------------------------------- #
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

# -------------------------------------------------------------------- #
# Function returns a list of sports currently supported
# -------------------------------------------------------------------- #
def sports(request):
	return render(request, 'sports.html', {'sports_dict':sports_dict})


# -------------------------------------------------------------------- #
# Function controls the search bar
# -------------------------------------------------------------------- #
def search(request):
	q = request.GET['term']
	results = []
	users = User.objects.filter(Q(first_name__icontains = q)|Q(last_name__icontains = q))[:6]
	names = q.split()
	if len(names) > 1:
		users = User.objects.filter(first_name__icontains = names[0], last_name__icontains = names[1])
	else:
		users = User.objects.filter( Q(first_name__icontains = names[0]) | Q(last_name__icontains = names[0]))		
	
	if users:
		for user in users:
			user_json = {}
			user_json['id'] = user.id
			user_json['value'] = user.get_full_name()
			user_json['label'] = user.get_full_name()
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

	sports = Sport.objects.filter(name__icontains = q )[:6]
	if sports:
		for sport in sports:
			sport_json = {}
			sport_json['id'] = sport.id
			sport_json['value'] = sport.name
			sport_json['label'] = sport.name
			sport_json['category'] = 'Sports'
			results.append(sport_json)		

	mimetype = 'application/json'
	return HttpResponse(json.dumps(results), mimetype)


# -------------------------------------------------------------------- #
# Function adds a comment to a game page
# -------------------------------------------------------------------- #
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

			comment = Comment.objects.create(text=text, commenter=commenter, game=game, timeStamp=datetime.datetime.now() - datetime.timedelta(hours=7))

			for player in game.users.all():
				if commenter != player:
					verb = commenter.first_name+' '+commenter.last_name+' left a comment for '+game.name
					description = '/game/'+str(game.id)
					notify.send(commenter,recipient=player, verb=verb, description=description)

			return redirect('/game/'+str(game.id))
		else:
			return redirect('/')
	else:
		return redirect('/')

# -------------------------------------------------------------------- #
# Function connects a users instragram profile to the user profile
# -------------------------------------------------------------------- #
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

# -------------------------------------------------------------------- #
# Function populates the photo upload choices in a game to the users
# instagram photos (if the user is connected to instagram)
# -------------------------------------------------------------------- #
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
	

# -------------------------------------------------------------------- #
# Function posts a photo to a game page
# -------------------------------------------------------------------- #
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


# -------------------------------------------------------------------- #
# Function uploads a profile photo to the users profile
# -------------------------------------------------------------------- #
@login_required
def upload_profile_photo(request):
	if request.method == 'POST':
		photo_url = request.POST['photo_url']
		user_info = UserInfo.objects.get(user=request.user)
		user_info.profile_picture = photo_url
		user_info.save()
		action.send(request.user,verb="profile photo",action_object=user_info)

	return redirect('/profile')

# -------------------------------------------------------------------- #
# Function toggles the follow of a user
# -------------------------------------------------------------------- #
@login_required
def toggle_follow(request):
	if request.method == 'POST':
		following_people= following(request.user)
		follow_username = request.POST['player']
		is_following = follow_username in following_people

		user = User.objects.get(username=follow_username)
		if not is_following:
			follow(request.user, user)
		else:
			unfollow(request.user, user)

		response = ""
		if is_following:
			response = "No"
		else:
			response = "Yes"

	# return HttpResponse(json.dumps(responseData),mimetype="application/json")
	return HttpResponse(response)


# -------------------------------------------------------------------- #
# Function controls the suggest pages you see at the bottom of the
# home page
# -------------------------------------------------------------------- #
@login_required
def analytics(request):
	# Player Analytics
	games_played = request.user.game_set.all()
	fav_sports = defaultdict(lambda:0)
	for game_played in games_played:
		fav_sports[game_played.sport.name] += 1
	fav_sports = sorted(fav_sports.iteritems(),key=lambda (k,v): v,reverse=True)

	# Sport Analytics
	freq_places = {}
	all_games = Game.objects.all()
	user = request.user
	for game in all_games:
		if game.sport.name in freq_places:
			freq_places[game.sport.name][game.location.name] += 1
		else:
			sport_loc = defaultdict(lambda:0)
			sport_loc[game.location.name] += 1
			freq_places[game.sport.name] = sport_loc

	sorted_freq_places = {}
	for k,places in freq_places.iteritems():
		sorted_places = sorted(places.iteritems(),key=lambda (k,v): v,reverse=True)
		sorted_freq_places[k] = sorted_places

	# Game Analytics
	all_games_played = Game.objects.filter(timeStart__lt=datetime.datetime.now()).order_by('-timeStart');
	games_played_breakdown = {}
	for game in all_games_played:
		if game.sport.name in games_played_breakdown:
			games_played_breakdown[game.sport.name] += 1
		else:
			games_played_breakdown[game.sport.name] = 1
	print games_played_breakdown

	return render(request, 'analytics.html', {
		'user' : user,
		'games_played'				: games_played,
		'fav_sports'				: fav_sports,
		'sorted_freq_places'		: sorted_freq_places,
		'all_games_played'			: all_games_played,
		'games_played_breakdown'	: games_played_breakdown
	})


# -------------------------------------------------------------------- #
# Function
# -------------------------------------------------------------------- #
@login_required
def first_login(request):
	if request.method == 'POST':
		print request.POST
		fav_sports = json.loads(request.POST.get('sports'))
		for sport_name in fav_sports.keys():
			sport = Sport.objects.get(name=sport_name)
			UserSportLevel.objects.create(user=request.user, sport=sport)

	return render(request, 'first_login.html', {'user':request.user})

# -------------------------------------------------------------------- #
# Function ???
# -------------------------------------------------------------------- #
@login_required
def first_login2(request):
	fav_sports = request.user.sport_set.all()
	if request.method == 'POST':
		for sport in fav_sports:
			user_sport = UserSportLevel.objects.filter(user=request.user, sport=sport)[0]
			user_sport.level = request.POST.get(sport.name)
			user_sport.save()

			return redirect('/home')

	return render(request, 'first_login2.html', {'user':request.user, 'fav_sports':fav_sports})

# -------------------------------------------------------------------- #
# Function ???
# -------------------------------------------------------------------- #
@login_required
def invite_friends(request, game_id):
	users = User.objects.all()
	if request.method == 'POST':
		invited_friends = request.POST.getlist('friends')
		print invited_friends

		if invited_friends:
			for friend in invited_friends:
				friend = User.objects.get(username=friend)
				if friend != request.user: 
					inviter = request.user.first_name + ' ' + request.user.last_name
					game = Game.objects.get(id=game_id)
					verb = inviter + ' invited you to join ' +game.name
					description = '/game/'+str(game.id)
					notify.send(request.user,recipient=friend, verb=verb, description=description)

		return redirect('/game/'+str(game_id)) 
		
	return render(request, 'invite_friends.html', {
		'users':users,
		'game_id':game_id,
		'user': request.user
	})


# -------------------------------------------------------------------- #
# Function ???
# -------------------------------------------------------------------- #
def get_fav_sports_set(request):
	fav_sports = request.user.sport_set.all()
	sports = set()
	sports_dict = defaultdict(lambda:0)
	for fav_sport in fav_sports:
		sports.add(fav_sport.name)
		user_sport = UserSportLevel.objects.get(user=request.user, sport=fav_sport)
		sports_dict[fav_sport.name] = user_sport.level
	
	return (sports, sports_dict)


def get_game_location_coordinates(game):
	return (game.location.latitude, game.location.longitude)

def get_user_location_coordinates(user):
	return (user.userinfo.latitude, user.userinfo.longitude)

def distance_on_unit_sphere(lat1, long1, lat2, long2):
	# Convert latitude and longitude to 
	# spherical coordinates in radians.
	degrees_to_radians = math.pi/180.0
	    
	# phi = 90 - latitude
	phi1 = (90.0 - lat1)*degrees_to_radians
	phi2 = (90.0 - lat2)*degrees_to_radians
	    
	# theta = longitude
	theta1 = long1*degrees_to_radians
	theta2 = long2*degrees_to_radians
	    
	# Compute spherical distance from spherical coordinates.
	    
	# For two locations in spherical coordinates 
	# (1, theta, phi) and (1, theta, phi)
	# cosine( arc length ) = 
	#    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
	# distance = rho * arc length

	cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
	       math.cos(phi1)*math.cos(phi2))
	arc = math.acos( cos )

	# Remember to multiply arc by the radius of the earth 
	# in your favorite set of units to get length.
	return arc*3963.1676

# -------------------------------------------------------------------- #
# Function ???
# -------------------------------------------------------------------- #
def get_game_recommendations(request):
	# weight factors and return the top 5 most 'relevant' games to user
	recommendations = defaultdict(lambda:0)
	(sports, sports_dict) = get_fav_sports_set(request)
	upcoming_games = Game.objects.filter(timeStart__gte=datetime.datetime.now()).order_by('timeStart');
	for upcoming_game in upcoming_games:
		if upcoming_game.creator != request.user:
			currSport = upcoming_game.sport
			weight = 0.0

			#Check for user's favorite sports
			if upcoming_game.sport.name in sports:
				creator_sports = upcoming_game.creator.sport_set.all()
				if currSport in creator_sports:
					creator_sport = UserSportLevel.objects.get(user=upcoming_game.creator, sport=currSport)
					creator_level = creator_sport.level
					if sports_dict[upcoming_game.sport.name] == creator_level:
						weight += 3
					else:
						weight += 2
				else:
					weight += 1

			# Check for game location
			(game_latitude, game_longitude) = get_game_location_coordinates(upcoming_game)	
			(user_latitude, user_longitude) = get_user_location_coordinates(request.user)
			distance = distance_on_unit_sphere(game_latitude, game_longitude, user_latitude, user_longitude)		
			weight += 1/distance
			
			# Check for game players' skill level + whether the user follows the player
			players_score = 0.0
			following_people = following(request.user)
			for player in upcoming_game.users.all():
				player_sport = UserSportLevel.objects.filter(user=player, sport=currSport)
				if player_sport.count():
					player_skill = player_sport[0]
					players_score += 1/(math.fabs(player_skill.level-sports_dict[upcoming_game.sport.name])+upcoming_game.users.count())

				if player in following_people:
					players_score += 0.5

			weight += players_score	
			recommendations[upcoming_game] = weight

	sorted_recommendations = sorted(recommendations.iteritems(), key=operator.itemgetter(1), reverse=True)
	print 'game recommendations'
	print sorted_recommendations
	return sorted_recommendations

# -------------------------------------------------------------------- #
# Function ???
# -------------------------------------------------------------------- #
def recommendations(request):
	game_recommendations = get_game_recommendations(request)

	return render(request, 'recommendations.html')

# -------------------------------------------------------------------- #
# Function ???
# -------------------------------------------------------------------- #
def store_user_location(request):
	if request.POST:
		latitude = request.POST.get('latitude')
		longitude = request.POST.get('longitude')

		user_info = UserInfo.objects.get(user=request.user)
		user_info.latitude = latitude
		user_info.longitude = longitude

		user_info.save()

	return HttpResponse('')


