# Generated by Django 4.1 on 2022-10-21 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0025_alter_ordermodel_additional_information_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='message',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]