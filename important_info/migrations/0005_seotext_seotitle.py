# Generated by Django 4.1 on 2022-10-15 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('important_info', '0004_alter_faqmodel_options_alter_pagemodel_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeoText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=2000)),
                ('text', models.TextField()),
                ('sorted_text', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Seo Text',
                'verbose_name_plural': 'Seo Text',
                'ordering': ('sorted_text',),
            },
        ),
        migrations.CreateModel(
            name='SeoTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=2000)),
            ],
            options={
                'verbose_name': 'Seo Title',
                'verbose_name_plural': 'Seo Title',
            },
        ),
    ]
