from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Location(models.Model):
	name = models.CharField(max_length=300)
	latitude = models.FloatField()
	longitude = models.FloatField()
	
class Sport(models.Model):
	name = models.CharField(max_length=200)
	lovers = models.ManyToManyField(User, through='UserSportLevel')

class Game(models.Model):
	#sport = models.CharField(max_length=50, null=True)
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=400)
	#location = models.CharField(max_length=300, null=True)
	dateCreated = models.DateTimeField(null=True)
	timeStart = models.DateTimeField(null=True)
	cap = models.IntegerField()
	# Need an owner (user) of the game
	creator = models.ForeignKey(User, related_name = "creator_of_game")
	location = models.ForeignKey(Location)
	users = models.ManyToManyField(User) # Game will have users that have signed up for the game
	sport = models.ForeignKey(Sport)

	@property
	def sorted_comment_set(self):
	    return self.comment_set.order_by('-timeStamp')

class Comment(models.Model):
	text = models.TextField()
	timeStamp = models.DateTimeField(null=True)
	game = models.ForeignKey(Game)
	commenter = models.ForeignKey(User)


class InstagramInfo(models.Model):
	# {u'access_token': u'1105726448.9135221.702125d2abb24aa49e410d1ac9c6fabc', 
	# u'user': 
	# {u'username': u'eymyers', u'bio': u'', u'website': u'', u'profile_picture': u'http://images.ak.instagram.com/profiles/anonymousUser.jpg', u'full_name': u'Ethan Myers', u'id': u'1105726448'}}

	access_token = models.CharField(max_length=200)
	username = models.CharField(max_length=200)
	profile_picture = models.CharField(max_length=200)
	full_name = models.CharField(max_length=200)
	instagramID = models.IntegerField()
	user = models.OneToOneField(User,null=False)

class GamePhoto(models.Model):
	thumbnail = models.URLField()
	standard = models.URLField()
	game = models.ForeignKey(Game)

class UserInfo(models.Model):
	profile_picture = models.URLField(default='http://fashionlawsymposium.com/wp-content/uploads/2013/10/person-placeholder.jpg')
	latitude = models.FloatField(null=True)
	longitude = models.FloatField(null=True)
	user = models.OneToOneField(User)

class UserSportLevel(models.Model):
	user = models.ForeignKey(User)
	sport = models.ForeignKey(Sport)
	level = models.IntegerField(default=0)
	