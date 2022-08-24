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
