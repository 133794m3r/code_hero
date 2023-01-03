"""
Code Hero Project
AGPLv3 or Later
Macarthur Inbody
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	id = models.AutoField(primary_key=True)
	points = models.IntegerField(default=0)
	tfa_enabled = models.BooleanField(default=False)
	tfa_secret = models.CharField(max_length=32,default=None,null=True)
	def to_dict(self):
		return {'id':self.id, 'username':self.username, 'email':self.email,
				'is_staff':self.is_staff, 'is_superuser':self.is_superuser,
				'first_name':self.first_name, 'last_name':self.last_name,
				'date_joined':self.date_joined, 'is_active':self.is_active,
				'last_login':self.last_login
		}

class Categories(models.Model):
	id = models.SmallAutoField(primary_key=True)
	name = models.CharField(max_length=50)
	class Meta:
		indexes = [ models.Index(fields=['name'])]

class Languages(models.Model):
	id = models.SmallAutoField(primary_key=True)
	name = models.CharField(max_length=30)

class ChallengeSolutions(models.Model):
	id = models.AutoField(primary_key=True)
	challenge_id = models.ForeignKey('Challenges',on_delete=models.CASCADE,related_name='id')
	language = models.ForeignKey('Languages',on_delete=models.CASCADE,related_name='language')
	code = models.TextField(max_length=4096)

class ChallengeCode(models.Model):
	id = models.AutoField(primary_key=True)
	language = models.ForeignKey('Languages',on_delete=models.CASCADE,related_name='language')
	base_code = models.TextField(max_length=4096)

class Challenges(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	description = models.TextField(max_length=2048)
	category = models.ForeignKey('Categories',on_delete=models.CASCADE,related_name='category')
	points = models.IntegerField()
	difficulty = models.SmallIntegerField()
	inputs = models.AutoField(max_length=1024)
	models.ManyToManyField(ChallengeCode)
