# Generated by Django 4.2.4 on 2023-09-03 16:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admin_panel', '0007_events_user_delete_speakers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='user',
        ),
        migrations.AddField(
            model_name='events',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
