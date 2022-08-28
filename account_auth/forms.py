from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password2')

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'has-ic',
            'placeholder': 'Name',
        }
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'has-ic',
            'placeholder': 'Email',
        }
    ))

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'has-ic',
            'placeholder': 'Password',
        }
    ))

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'email', 
            'password1'
        ]


class SignInForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'has-ic',
            'id': 'id_email',
            'placeholder': 'Email',
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'has-ic',
            'placeholder': 'Password',
        }
    ))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())