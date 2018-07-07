from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.home, name='home'),
 	url(r'^service/', views.service, name='service'),
 	url(r'^addService/', views.addService, name='addService'),
 	url(r'^searchService/', views.searchService, name='searchService'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
