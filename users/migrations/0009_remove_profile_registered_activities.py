# Generated by Django 4.2.1 on 2023-07-22 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_profile_registered_activities'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='registered_activities',
        ),
    ]
