from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', views.home, name='home'),
 	url(r'^input/', views.input, name='input'),
 	url(r'^addService/', views.addService, name='input'),
 	
       
]