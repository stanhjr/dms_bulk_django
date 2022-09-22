from django.db import migrations

from order.models import ServicesUnderMaintenance


def create_default_services_under_maintenance(*args, **kwargs):
    services_under_maintenance = ServicesUnderMaintenance.objects.create()
    services_under_maintenance.save()


class Migration(migrations.Migration):
    dependencies = [
        ('order', '0021_alter_servicesundermaintenance_discord_and_more'),
    ]
    operations = [
        migrations.RunPython(create_default_services_under_maintenance),
    ]
