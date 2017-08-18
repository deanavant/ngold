from django.conf.urls import url
from . import views

def test(request):
	print "second urls.py"

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
]