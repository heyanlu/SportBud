# Generated by Django 4.2.1 on 2023-07-19 13:54

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_profile_first_name'),
        ('base', '0018_remove_activity_joined_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='signed_up_users',
        ),
        migrations.AddField(
            model_name='activity',
            name='end_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='events', to='users.profile'),
        ),
        migrations.AddField(
            model_name='activity',
            name='registration_deadline',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='start_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='scheduled_date',
            field=models.DateTimeField(),
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('details', models.TextField(null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('activity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.activity')),
                ('participant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='submissions', to='users.profile')),
            ],
        ),
    ]
