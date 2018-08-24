from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
 	url(r'home/$', views.displayCarsProperties, name='displayCarsProperties'),
 	url(r'^addCars/$', views.addCars, name='addCars'),
 	url(r'^home/ajax/displayModels/$', views.displayModels, name='displayModels'),
 	url(r'^displayCars/$', views.displayCars, name='displayCars'),
 	url(r'^displayMore/$', views.displayMore, name='displayCars'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
