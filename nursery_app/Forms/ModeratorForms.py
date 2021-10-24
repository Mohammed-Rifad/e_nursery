from django import forms
from django.db.models import fields
from ..models import *
import re


class ChangePasswordForm(forms.Form):
    old_passwd=forms.CharField(label="Old Password",widget=forms.PasswordInput(attrs={'class':'form-control','style':'width:300px'}))
    new_passwd=forms.CharField(label="New Password",widget=forms.PasswordInput(attrs={'class':'form-control','style':'width:300px'}))
    confirm_passwd=forms.CharField(label="Confirm Password",widget=forms.PasswordInput(attrs={'class':'form-control','style':'width:300px'}))
