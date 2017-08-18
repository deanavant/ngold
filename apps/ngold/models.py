# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ..login_app.models import *

class Activity(models.Model):
	value = models.CharField(max_length=100)
	player_id = models.ForeignKey(User,related_name="player_activity")