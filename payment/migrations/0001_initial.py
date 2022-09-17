# Generated by Django 4.1 on 2022-09-15 15:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_id', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(choices=[('Paid', 'Paid'), ('Awaiting Payment', 'Awaiting Payment')], default='Awaiting Payment', max_length=50)),
                ('payment_method', models.CharField(choices=[('Paypal', 'Paypal'), ('CreditCard', 'CreditCard')], max_length=50)),
                ('cents', models.BigIntegerField(blank=True, null=True)),
                ('description', models.CharField(default='Social Media Marketing', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]