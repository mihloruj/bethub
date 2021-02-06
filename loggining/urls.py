from django.urls import path

from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path('', userMain, name='usermain'),
    path('login/', userLogin, name='login'),
    path('logout/', userLogout, name='logout'),
    path('register/', userRegister, name='register'),
    path('profile/', userProfile, name='profile'),
    
    path('choicesub/', userChoiseSub, name='choicesub'),
    path('prolongationsub/', userReSub, name='resub'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name= "loggining/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name= "loggining/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name= "loggining/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name= "loggining/password_reset_done.html"), name="password_reset_complete"),
]