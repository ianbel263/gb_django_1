# Generated by Django 3.2.9 on 2021-12-13 10:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_auto_20211213_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activation_key_expires_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 12, 15, 10, 43, 35, 391510, tzinfo=utc), null=True),
        ),
    ]
