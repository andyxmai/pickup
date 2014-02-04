from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Location(models.Model):
	name = models.CharField(max_length=300)
	latitude = models.FloatField()
	longitude = models.FloatField()

class Game(models.Model):
	sport = models.CharField(max_length=50, null=True)
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=400)
	location = models.CharField(max_length=300, null=True)
	dateCreated = models.DateTimeField(null=True)
	timeStart = models.DateTimeField(null=True)
	# Need an owner (user) of the game
	creator = models.ForeignKey(User, related_name = "creator_of_game")
	location = models.ForeignKey(Location)
	users = models.ManyToManyField(User) # Game will have users that have signed up for the game

	