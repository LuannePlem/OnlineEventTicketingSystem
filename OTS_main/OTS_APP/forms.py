from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=False)
    age = forms.IntegerField(max_value=120, required=False)
    

    class Meta:
        model = User  # use your custom user
        fields = ['username', 'email', 'first_name', 'last_name', 'age', 'password1', 'password2']
    