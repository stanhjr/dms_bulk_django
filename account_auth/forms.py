from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms

from account.models import CustomUser


class SignUpForm(forms.ModelForm):
    class Meta:
        model = CustomUser
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


class SignInForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields.pop('username')

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'has-ic',
                'placeholder': 'Email',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'has-ic',
                'placeholder': 'Password',
            }) 
        }