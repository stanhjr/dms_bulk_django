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
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Awaiting Payment')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD)
    cents = models.BigIntegerField(null=True, blank=True)
    description = models.CharField(max_length=255, default='Social Media Marketing')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='invoice')

    class Meta:
        ordering = ['created_at']

    @property
    def cost(self):
        return self.cost * 100

    def save(self, *args, **kwargs):
        self.invoice_id = f'DM-{self.user_id}-{self.id}'

        super(Invoice, self).save(*args, **kwargs)

    # @receiver(post_save, sender=Invoice, dispatch_uid="update_stock_count")
    # def update_stock(sender, instance, **kwargs):
    #     instance.product.stock -= instance.amount
    #     instance.product.save()

