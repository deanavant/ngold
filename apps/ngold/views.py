# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
import random, time
from ..login_app.models import *

def index(request):
	if isAuth():
		try:
			request.session['gold']
		except:
			request.session['gold'] = 0

		user = User.objects.get(id=request.session['player_id'])
		request.session['gold'] = user.gold
		results = User.objects.GetTopFivePlayers()
		context = { 'players': results }
		print "player logged in is {}".format(request.session['player_id'])
		
		return render(request,'ngold/index.html',context)

def logout(request):
	request.session['logged_in'] = False
	user = User.objects.get(id=request.session['player_id'])
	user.gold = request.session['gold']
	user.save()
	return redirect("/")

def all_players(request):
	if isAuth():
		results = User.objects.GetAllPlayers()
		context = { 'players': results }
		return render(request,'ngold/players.html',context)

def play(request):
	if isAuth():
		return render(request,'ngold/play.html')

def player(request,kwarg):
	if isAuth():
		user = User.objects.get(id=kwarg)
		context = { 'player_name': user.email, 'player_gold': user.gold }
		return render(request,'ngold/player.html',context)

def process_gold(request):
	choice = request.POST['building']

	value = 0;
	if choice == 'cave':
		value = random.randint(-5,5)
	elif choice == 'castle':
		value = random.randint(-10,10)
	else:  # must be farm otherwise
		value = random.randint(-1,1)

	request.session['gold'] += value
	return redirect("/ngold/play")

def isAuth():
	try:
		if request.session['logged_in'] == True:
			return True
	except:
		return redirect("/")
	return redirect("/")