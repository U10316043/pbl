# _*_ coding:utf-8 _*_
from django import forms
from .models import ExtraProfile

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)
    
class RegisterForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)
    
class UploadImageForm(forms.ModelForm):
    class Meta:
        model = ExtraProfile
        fields = ['image']