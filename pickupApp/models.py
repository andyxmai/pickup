from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Game(models.Model):
	sport = models.CharField(max_length=50, null=True)
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=400)
	latitude = models.FloatField()
	longitude = models.FloatField()
	users = models.ManyToManyField(User)

	