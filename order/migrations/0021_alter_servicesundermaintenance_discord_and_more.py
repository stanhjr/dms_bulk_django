# Generated by Django 4.1 on 2022-09-22 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0020_servicesundermaintenance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicesundermaintenance',
            name='discord',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='servicesundermaintenance',
            name='instagram',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='servicesundermaintenance',
            name='telegram',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='servicesundermaintenance',
            name='twitter',
            field=models.BooleanField(default=False),
        ),
    ]