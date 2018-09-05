from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.home, name='home'),
 	url(r'^service/$', views.service, name='service'),
 	url(r'^addService/$', views.addService, name='addService'),
 	url(r'^searchService/$', views.searchService, name='searchService'),
 	url(r'^signup/$', views.register_user, name='signup'),
 	url(r'^login/$', auth_views.login, name="login"),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^password-change/$', views.password_change, name='password_change'),
    url(r'^object/$', views.viewObject, name='object'),
    url(r'^ajax/addComment/$', views.addComment, name='addComment'),
    url(r'^ajax/deleteComment/$', views.deleteComment, name='deleteComment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
