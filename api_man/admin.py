from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Country)
admin.site.register(AvaiablePlatformServiceByCountry)
admin.site.register(PlatformImage)
