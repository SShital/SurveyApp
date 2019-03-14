"""
form classes
"""
from django import forms


class LoginForm(forms.Form):
    """
    login-form details
    """
    username = forms.CharField(max_length=40,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'password'}))
