from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms
from django.contrib.auth import get_user_model


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=False)
    age = forms.IntegerField(max_value=120, required=False)
    USER_TYPES = [
        ('User', 'User'),
        ('Manager', 'Manager'),
    ]
    usertype = forms.ChoiceField(choices=USER_TYPES, label='User Type')

    class Meta:
        model = get_user_model() 
        fields = ['username', 'email', 'first_name', 'last_name', 'age', 'usertype', 'password1', 'password2']
