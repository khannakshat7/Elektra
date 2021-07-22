from django.contrib import admin
from electricity.models import electricity,Contact,FeedBack,electricity
from import_export.admin import ImportExportModelAdmin
# Register your models here.
# admin.site.register(electricity)
#Registered Contact model
# admin.site.register(Contact)
# admin.site.register(FeedBack)

@admin.register(FeedBack)
class FeedBackAdmin(ImportExportModelAdmin):
    pass
@admin.register(Contact)
class ContactAdmin(ImportExportModelAdmin):
    pass
@admin.register(electricity)
class UserAdmin(ImportExportModelAdmin):
    pass