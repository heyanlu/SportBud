# Generated by Django 4.2.1 on 2023-07-14 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_activity_vote_ratio_alter_activity_vote_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='vote_ratio',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3),
        ),
    ]