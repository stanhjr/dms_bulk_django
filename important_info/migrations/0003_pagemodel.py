# Generated by Django 4.1 on 2022-09-28 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('important_info', '0002_add_default_faq'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
            ],
        ),
    ]