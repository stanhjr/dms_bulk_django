from django import forms
from django.core.exceptions import ValidationError

from payment.models import Invoice


class CreateInvoiceCalcForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ('payment_method', 'cents')

    def clean(self):
        if not self.cleaned_data.get('cents') or not self.cleaned_data.get('payment_method'):
            raise ValidationError("no fields")

        return self.cleaned_data
