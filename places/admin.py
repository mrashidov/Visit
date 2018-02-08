from django.contrib import admin
from places.models import *
# Register your models here.
admin.site.register(Place)
admin.site.register(City)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Schedule)
admin.site.register(PlacePhoneNumber)
admin.site.register(PlaceFeature)
admin.site.register(PlacePhoto)
