# Generated by Django 4.1 on 2022-09-20 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0018_ordermodel_hours_to_sending_end'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='screenshot_complete',
            field=models.ImageField(blank=True, null=True, upload_to='screenshot_complete_images/'),
        ),
    ]