# Generated by Django 3.2.21 on 2023-09-22 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_delete_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='actions_taken',
            field=models.TextField(blank=True),
        ),
    ]