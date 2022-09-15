from email.policy import default
from django import forms

from . import models


class CreateOrderCalcForm(forms.ModelForm):
    class Meta:
        model = models.OrderCalcModel
        fields = ('social_network', 'amount', 'discount', 'total')


class CreateOrderForm(forms.ModelForm):
    use_dms_tokens = forms.BooleanField(required=False)

    class Meta:
        model = models.OrderModel
        fields = ('targets_or_competitors_submited',
                  'use_our_default_filtering',
                  'not_use_any_filtering',
                  'message',
                  'attach_in_message',
                  'additional_information',
                  'contact_details')
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
