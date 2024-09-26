from django.contrib import admin
from UserInfo.models import TutleeUser

class customizeAdminManager(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'created_by', 'address']

admin.site.register(TutleeUser, customizeAdminManager)


