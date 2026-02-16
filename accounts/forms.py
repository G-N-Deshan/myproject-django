from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    full_name = forms.CharField(max_length=150)
    address = forms.CharField(max_length=255)
    phone = forms.CharField(max_length=20)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
        
class LoginForm(AuthenticationForm):
    pass 