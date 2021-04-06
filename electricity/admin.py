from django.contrib import admin
from electricity.models import electricity,Contact,Location
# Register your models here.
admin.site.register(electricity)
#Registered Contact model
admin.site.register(Contact)
admin.site.register(Location)
