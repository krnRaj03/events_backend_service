# Generated by Django 4.2.4 on 2023-08-30 17:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_address_id_remove_address_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_id',
            field=models.UUIDField(default=uuid.UUID('6929ed50-41aa-40ee-a6da-3aecd0fc41cd'), primary_key=True, serialize=False),
        ),
    ]
