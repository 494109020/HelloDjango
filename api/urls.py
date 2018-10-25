"""api"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^userlist/$', views.userlist, name="userlist"),
    url(r'^topiclist/$', views.topiclist, name="topiclist"),
    url(r'^topiclist1/$', views.topiclist1, name="topiclist1"),
    url(r'^entrylist/$', views.entrylist, name="entrylist"),
]
