# Generated by Django 4.0.6 on 2023-04-28 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment_info', '0012_alter_submissions_checked_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submissions',
            name='checked_by',
            field=models.CharField(blank=True, default='Not checked yet', max_length=30),
        ),
    ]