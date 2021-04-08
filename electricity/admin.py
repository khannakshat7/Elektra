from django.contrib import admin
from electricity.models import electricity,Contact,Feedback
# Register your models here.
admin.site.register(electricity)
#Registered Contact model
admin.site.register(Contact)
# register feedback model
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    ordering = ('-date_posted',)
    readonly_fields  = ('date_posted',)
    list_display = ('user_email',)