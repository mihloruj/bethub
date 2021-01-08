from django import forms
from django.forms import CharField, PasswordInput, EmailInput
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

        # Нужно убрать возможность пробелов, и наверное отключить сравнение с именем и емайлом,
        # запретить вставлять текст
        # Или вообще написать свои валидаторы 
class CreateUserForms(UserCreationForm):
    username = forms.CharField(
        required=True,
        label='Логин',
        min_length=5, 
        max_length=50, 
        error_messages={
            'required': 'Укажите логин',
            'max_length': 'Логин должен быть не более 50 символов',
            'min_length': 'Логин должен быть более 5 символов'
        })
    email = forms.EmailField(
        required=True,
        label='Email', 
        widget=EmailInput(),
        max_length=100,
        error_messages={
            'required': 'Укажите email',
            'invalid': 'Email указан неверно'
            })
    password1 = forms.CharField(
        required=True,
        label='Пароль', 
        widget=PasswordInput(),
        max_length=25, 
        error_messages={
            'required': 'Укажите пароль',
            'max_length': 'Логин должен быть не более 25 символов',
            'min_length': 'Логин должен быть более 8 символов'
        })
    password2 = forms.CharField(
        required=True,
        label='Пароль (еще раз)', 
        widget=PasswordInput(),
        max_length=25, 
        error_messages={
            'required': 'Введите повторно пароль',
            'max_length': 'Пароль должен быть не более 25 символов',
            'min_length': 'Пароль должен быть более 8 символов'
        })
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserChangePassword(PasswordChangeForm):
    old_password = forms.CharField(
        required=True,
        label='Старый пароль', 
        widget=PasswordInput(),
        max_length=25, 
        error_messages={
            'required': 'Укажите пароль',
            'max_length': 'Логин должен быть не более 25 символов',
            'min_length': 'Логин должен быть более 8 символов'
        })
    new_password1 = forms.CharField(
        required=True,
        label='Новый пароль', 
        widget=PasswordInput(),
        max_length=25, 
        error_messages={
            'required': 'Введите повторно пароль',
            'max_length': 'Пароль должен быть не более 25 символов',
            'min_length': 'Пароль должен быть более 8 символов'
        })
    new_password2 = forms.CharField(
        required=True,
        label='Новый пароль (еще раз)', 
        widget=PasswordInput(),
        max_length=25, 
        error_messages={
            'required': 'Введите повторно пароль',
            'max_length': 'Пароль должен быть не более 25 символов',
            'min_length': 'Пароль должен быть более 8 символов'
        })
    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']