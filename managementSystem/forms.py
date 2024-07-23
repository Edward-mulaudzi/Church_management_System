from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class LoginForm(forms.Form):
    username= forms.CharField(widget=forms.TextInput())
    password= forms.CharField(widget=forms.PasswordInput())

class AddUserForm(UserCreationForm):
    username= forms.CharField(label='',widget=forms.TextInput(attrs={'class':'field','placeholder':'Username'}))
    password1= forms.CharField(label='',widget=forms.PasswordInput(attrs={'class':'field','placeholder':'Password'}))
    password2= forms.CharField(label='',widget=forms.PasswordInput(attrs={'class':'field','placeholder':'Confirm Password'}))
    email= forms.EmailField(label='',widget=forms.EmailInput(attrs={'class':'field','placeholder':'Email'},))

    class Meta:
        model=User
        fields= ('username','email','password1','password2', 'branch','is_superuser', 'is_admin', 'is_user')
        

class AdminAddUserForm(UserCreationForm):
    username= forms.CharField(label='',widget=forms.TextInput(attrs={'class':'field','placeholder':'Username'}))
    password1= forms.CharField(label='',widget=forms.PasswordInput(attrs={'class':'field','placeholder':'Password'}))
    password2= forms.CharField(label='',widget=forms.PasswordInput(attrs={'class':'field','placeholder':'Confirm Password'}))
    email= forms.EmailField(label='',widget=forms.EmailInput(attrs={'class':'field','placeholder':'Email'},))

    class Meta:
        model=User
        fields= ('username','email','password1','password2', 'is_admin', 'is_user')
