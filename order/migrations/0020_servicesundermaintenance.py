# Generated by Django 4.1 on 2022-09-22 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0019_ordermodel_screenshot_complete'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServicesUnderMaintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instagram', models.BooleanField(default=True)),
                ('twitter', models.BooleanField(default=True)),
                ('discord', models.BooleanField(default=True)),
                ('telegram', models.BooleanField(default=True)),
            ],
        ),
    ]