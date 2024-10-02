from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.views import TokenObtainPairView
from UserInfo.views import *

urlpatterns=[
    path('signUp/', register_user,name = 'signUp'),
    path('gettoken/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('varify/', TokenVerifyView.as_view()),
    path('login/', login_user,name = 'login'),
    path('studentDetail/<int:pk>', GetSinglestudent.as_view(), name = 'studentDetail'),
    path('updateStudentProfile/<int:pk>', UpdateStudent.as_view(), name = 'updateUser'),
    path('DeleteStudentProfile/<int:pk>', DeleteStudent.as_view(), name = 'DeleteStudentProfile'),
    # Additional Info
    path('AddAdditionalInfo/<int:pk>', AddAdditionalInfo.as_view(), name = 'AddAdditionalInfo'),
    path('UpdateAdditionalInfo/<int:pk>', UpdateAdditionalInfo.as_view(), name = 'UpdateAdditionalInfo'),
    path('GetStudentAdditionalInfo/<int:pk>', GetStudentAdditionalInfo.as_view(), name = 'GetStudentAdditionalInfo'),
    path('DeleteAdditionalInfo/<int:pk>', DeleteAdditionalInfo.as_view(), name = 'DeleteAdditionalInfo'),
    ]