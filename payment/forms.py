from django import forms

from payment.models import Invoice


class CreateOrderCalcForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ('payment_method', 'cents')
