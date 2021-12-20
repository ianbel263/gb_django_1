# Generated by Django 3.2.9 on 2021-12-20 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0006_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='language',
            field=models.CharField(blank=True, choices=[('en', 'english'), ('ru', 'русский')], max_length=2, verbose_name='язык'),
        ),
    ]