# Generated by Django 4.1 on 2022-08-29 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_articlemodel_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlemodel',
            name='content_text',
            field=models.TextField(max_length=100000),
        ),
    ]
