from django.contrib import admin
from electricity.models import electricity,Contact,FeedBack
# Register your models here.
admin.site.register(electricity)
#Registered Contact model
admin.site.register(Contact)
admin.site.register(FeedBack)
