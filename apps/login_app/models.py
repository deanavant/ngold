# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re, bcrypt

ereg = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
	def ValidateReg(self,postData):
		results = { 'status':False, 'errors':[] }

		if len(postData['first_name']) < 3:
			results['errors'].append("First name must be 3 or more characters")
		elif not postData['first_name'].isalpha():
			results['errors'].append("First name must be alpha characters only")
		if len(postData['last_name']) < 3:
			results['errors'].append("Last name must be 3 or more characters")
		elif not postData['last_name'].isalpha():
			results['errors'].append("Last name must be alpha characters only")
		if len(postData['email']) == 0:
			results['errors'].append("Email must not be blank")
		elif not(ereg.match(postData['email'])):
			results['errors'].append("Invalid email format (eg. xx@xx.xxx)")
		elif User.objects.filter(email=postData['email']).count() != 0:
			results['errors'].append("Email {} already registered".format(postData['email']))
		if len(postData['password']) < 8:
			results['errors'].append("Password must be 8 or more characters")
		if postData['password'] != postData['pwc']:
			results['errors'].append("Passwords must match")

		results['status'] = len(results['errors']) != 0
		print User.objects.all().count()
		return results

	def ValidateLog(self,postData):
		results = { 'status':False, 'errors':[] }
		query = User.objects.filter(email=postData['email'])
		if query.count() == 0:
			results['errors'].append("Did not find user in database")
		else:
			user = query.first()
			if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
				results['errors'].append("User password did not match")
		results['status'] = len(results['errors']) != 0
		return results

	def CreateUser(self,postData):
		hashpw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
		user = User.objects.create(first_name=postData['first_name'],
			last_name=postData['last_name'],
			email=postData['email'],
			password=hashpw)
		return user

	def GetTopFivePlayers(self):
		query = User.objects.raw("SELECT id, email, gold FROM login_app_User ORDER BY gold DESC LIMIT 5")
		results = []
		for user in query:
			result = '<tr><td><a href="/ngold/{}/player">{}</a></td>'.format(user.id,user.email)
			result += "<td>{}</td></tr>".format(user.gold)
			results.append(result)
		return results

	def GetAllPlayers(self):
		query = User.objects.all()
		results = []
		for user in query:
			result = '<tr><td><a href="/ngold/{}/player">{}</a></td>'.format(user.id,user.email)
			result += "<td>{}</td></tr>".format(user.gold)
			results.append(result)
		return results

class User(models.Model):
	first_name = models.CharField(max_length=55)
	last_name = models.CharField(max_length=55)
	email = models.CharField(max_length = 55)
	password = models.CharField(max_length = 100)
	gold = models.IntegerField(default = 0)
	created_at = models.DateField(auto_now_add=True)
	objects = UserManager()
