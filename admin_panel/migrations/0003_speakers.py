# Generated by Django 4.2.4 on 2023-09-01 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0002_events_venue_organizer_address_line1_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Speakers',
            fields=[
                ('speaker_id', models.AutoField(primary_key=True, serialize=False)),
                ('speaker_name', models.CharField(max_length=100)),
                ('speaker_description', models.CharField(max_length=100)),
                ('speaker_email', models.EmailField(max_length=100)),
                ('speaker_mobile_no', models.CharField(max_length=10)),
                ('speaker_address_line1', models.CharField(max_length=100)),
                ('speaker_address_line2', models.CharField(max_length=100)),
                ('speaker_city', models.CharField(max_length=100)),
                ('speaker_state', models.CharField(max_length=100)),
                ('speaker_country', models.CharField(max_length=100)),
                ('speaker_pincode', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('events_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.events')),
            ],
        ),
    ]
