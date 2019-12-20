from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(min_length=3, max_length=150)

    class Meta:
        model = CustomUser
        fields = ['username', 'email']


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')
