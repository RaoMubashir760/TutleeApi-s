from django.contrib import admin
from django.urls import path
from django.urls import include
from UserInfo.views import * 

urlpatterns = [
                path('admin/', admin.site.urls),
                path('api/', include('UserInfo.urls')),
               ]