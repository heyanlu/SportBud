# Generated by Django 4.2.1 on 2023-07-18 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_alter_activity_options_review_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='user_tags',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]