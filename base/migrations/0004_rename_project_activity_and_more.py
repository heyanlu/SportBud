# Generated by Django 4.2.1 on 2023-07-08 01:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_remove_review_tags_remove_review_vote_ratio_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Project',
            new_name='Activity',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='project',
            new_name='activity',
        ),
    ]