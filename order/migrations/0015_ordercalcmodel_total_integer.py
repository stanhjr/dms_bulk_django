# Generated by Django 4.1 on 2022-09-19 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_alter_boardmodel_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordercalcmodel',
            name='total_integer',
            field=models.IntegerField(null=True),
        ),
    ]