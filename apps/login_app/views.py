# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from models import *

def index(request):
	request.session['logged_in'] = False
	
	return render(request, 'login_app/index.html')

def register(request):
	results = User.objects.ValidateReg(request.POST)
	if results['status']:
		for error in results['errors']:
			messages.add_message(request, messages.INFO, error)
	else:
		messages.add_message(request, messages.INFO, "Registration of {} successful".format(request.POST['email']))
		user = User.objects.CreateUser(request.POST)
		user.save()

	return redirect("/")

def login(request):
	results = User.objects.ValidateLog(request.POST)
	if results['status']:
		for error in results['errors']:
			messages.add_message(request, messages.INFO, error)
	else:
		user = User.objects.get(email=request.POST['email'])
		request.session['logged_in'] = True
		request.session['player_id'] = user.id
		return redirect("/ngold/")

	return redirect("/")