from django import forms

from . import models


class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = models.OrderModel
        fields = '__all__'
        widgets = {
            'targets_or_competitors_submited': forms.Textarea(
                attrs={
                    'placeholder': 'Type here...',
                    'maxlength': '2000'
                }
            ),
            'message': forms.Textarea(
                attrs={
                    'placeholder': 'Type here...',
                    'maxlength': '1000',
                    'class': 'js-textarea-max'
                }
            ),
            'attach_in_message': forms.Textarea(
                attrs={
                    'placeholder': 'Type here...',
                    'maxlength': '600',
                    'class': 'js-textarea-max'
                }
            ),
            'additional_information': forms.Textarea(
                attrs={
                    'placeholder': 'Type here...',
                    'maxlength': '600',
                    'class': 'js-textarea-max'
                }
            ),
            'contact_details': forms.TextInput(
                attrs={
                    'placeholder': 'Type here...'
                }
            )
        }
