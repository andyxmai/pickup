from django.db import models

# Create your models here.
class User(models.Model):
	first_name = models.CharField(max_length=200, null=True)
	last_name = models.CharField(max_length=200, null=True)
	email = models.EmailField()
	password = models.CharField(max_length=50)

class Games(models.Model):
	sport = models.CharField(max_length=50, null=True)
	