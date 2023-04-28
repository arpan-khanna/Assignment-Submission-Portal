# Generated by Django 4.0.6 on 2023-04-28 18:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assignment_info', '0010_regusers'),
    ]

    operations = [
        migrations.AddField(
            model_name='submissions',
            name='checked_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='checked_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='submissions',
            name='feedback',
            field=models.TextField(blank=True, default='No feedback'),
        ),
    ]
