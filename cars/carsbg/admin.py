from django.contrib import admin
from .models import *
#from django_google_maps import widgets as map_widgets
#from django_google_maps import fields as map_fields

"""class RentalAdmin(admin.ModelAdmin):
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }
"""
admin.site.register(City)
admin.site.register(Service)
admin.site.register(CarDealer)
admin.site.register(Comment)
admin.site.register(Article)
