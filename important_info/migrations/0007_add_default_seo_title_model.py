from django.db import migrations
from important_info.models import SeoTitle


def create_model(apps, schema_editor):
    SeoTitle.objects.create(title='Mass DM Services - DMSBulk')


class Migration(migrations.Migration):
    dependencies = [
        ('important_info', '0006_remove_seotext_title_seotext_name_for_admin'),
    ]

    operations = [
        migrations.RunPython(create_model),
    ]
