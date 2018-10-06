from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^service/$', views.object, name='service'),
    url(r'^search/$', views.search, name='search'),
 	url(r'^addService/$', views.addService, name='addService'),
 	url(r'^searchService/$', views.searchService, name='searchService'),
 	url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login_user, name="login"), 
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^password-change/$', views.password_change, name='password_change'),
    url(r'^viewObject/$', views.viewObject, name='object'),
    url(r'^ajax/addComment/$', views.addComment, name='addComment'),
    url(r'^ajax/deleteComment/$', views.deleteComment, name='deleteComment'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^setImage/$', views.setImage, name='setImage'),
   	url(r'^displayService/(?P<pk>\w{0,50})/$', views.displayService, name='displayService'),
   	url(r'^settings/$', views.settings, name='settings'),
    url(r'^settings/password/$', views.password, name='password'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
