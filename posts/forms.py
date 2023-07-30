from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=128)
    password1 = forms.CharField(max_length=32)
    password2 = forms.CharField(max_length=32)
    name = forms.CharField(max_length=32)
    age = forms.IntegerField()

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', 'name', 'age']

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=128, required=True, widget=forms.EmailInput)
    password = forms.CharField(max_length=32, required=True, widget=forms.PasswordInput)