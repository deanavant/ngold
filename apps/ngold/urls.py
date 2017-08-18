from django.conf.urls import url
from . import views

def test(request):
	print "ngold urls.py"

urlpatterns = [
	url(r'^logout$', views.logout),
	url(r'^all_players$', views.all_players),
	url(r'^play$', views.play),
	url(r'^process_gold$', views.process_gold),
	url(r'^(?P<kwarg>\d+)/player$', views.player),
    url(r'^$', views.index),
]