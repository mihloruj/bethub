from django.urls import path
from .views import *

urlpatterns = [
    path('', userMain, name='usermain'),
    path('login/', userLogin, name='login'),
    path('logout/', userLogout, name='logout'),
    path('register/', userRegister, name='register'),
    path('resetpassword/', userResetpswd, name='resetpswd'),
    path('choicesub/', userChoiseSub, name='choicesub'),
]