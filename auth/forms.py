from django.contrib.auth.models import User
from django import forms


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'has-ic',
                'placeholder': 'Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'has-ic',
                'placeholder': 'Email',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'has-ic',
                'placeholder': 'Password',
            }) 
        }