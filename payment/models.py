from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Invoice(models.Model):
    STATUS_CHOICES = (
        ('Paid', 'Paid'),
        ('Awaiting Payment', 'Awaiting Payment')
    )
    PAYMENT_METHOD = (
        ('Paypal', 'Paypal'),
        ('CreditCard', 'CreditCard')
    )

    invoice_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='Awaiting Payment')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD)
    cents = models.BigIntegerField(blank=True, null=True)
    description = models.CharField(
        max_length=255, default='Social Media Marketing')
    created_at = models.DateTimeField(auto_now_add=True)
    complete_at = models.DateField(null=True, blank=True)
    stripe_invoice_id = models.CharField(max_length=1000, null=True, blank=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='invoice')

    class Meta:
        ordering = ('-created_at', )

    @property
    def cost(self):
        return self.cents / 100

    def save(self, *args, **kwargs):
        self.invoice_id = f'DM-{self.user_id}-{self.id}'
        super(Invoice, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.invoice_id} by {self.user} {self.payment_method}'

