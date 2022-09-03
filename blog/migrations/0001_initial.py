# Generated by Django 4.1 on 2022-09-03 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
                ('content_text', models.TextField(max_length=100000)),
                ('preview_text', models.CharField(max_length=130)),
                ('content_image', models.ImageField(upload_to='content_images/')),
                ('preview_image', models.ImageField(upload_to='preview_images/')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]
