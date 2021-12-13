# Generated by Django 3.2.9 on 2021-12-13 10:44

import authapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0003_alter_user_activation_key_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activation_key_expires_at',
            field=models.DateTimeField(blank=True, default=authapp.models.get_expire_time, null=True),
        ),
    ]
