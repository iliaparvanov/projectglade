from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
 	url(r'articlePage/$', views.articlePage, name='articlePage'),
 	url(r'articleText/$', views.articleText, name='articleText'),
 	url(r'$', views.displayArticles, name='displayArticles'),
 	url(r'addArticle/$', views.addArticle, name='addArticle'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
