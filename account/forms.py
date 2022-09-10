from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django import forms


class EmailSettingsForm(forms.ModelForm):
    receive_news = forms.BooleanField(
        required=False, widget=forms.CheckboxInput())
    receive_activity = forms.BooleanField(
        required=False, widget=forms.CheckboxInput())

    def __init__(self, *args, **kwargs):
        receive_news_initial = kwargs.pop('receive_news_initial')
        receive_activity_initial = kwargs.pop('receive_activity_initial')
        super().__init__(*args, **kwargs)
        self.fields['receive_news'].initial = receive_news_initial
        self.fields['receive_activity'].initial = receive_activity_initial

    class Meta:
        model = get_user_model()
        fields = ('receive_news', 'receive_activity')


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password'
        }
    ))
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password'
        }
    ))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password'
        }
    ))


class RestorePasswordChangeForm(PasswordChangeForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password'
        }
    ))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password'
        }
    ))