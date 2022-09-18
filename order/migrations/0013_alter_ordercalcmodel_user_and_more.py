# Generated by Django 4.1 on 2022-09-18 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0012_coupon_uses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordercalcmodel',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='order_calc',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='order_model', to='order.ordercalcmodel'),
        ),
    ]
