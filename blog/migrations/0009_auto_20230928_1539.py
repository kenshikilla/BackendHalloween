# Generated by Django 3.2.21 on 2023-09-28 09:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0008_ticket_actions_taken'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='assigned_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_tickets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ticket',
            name='resolved_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resolved_tickets', to=settings.AUTH_USER_MODEL),
        ),
    ]
