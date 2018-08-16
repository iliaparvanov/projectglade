from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
 	url(r'home/$', views.carsCompare, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
