# Generated by Django 4.0.6 on 2023-04-27 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assignment_info', '0007_alter_course_code_course_unique_course_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cname',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('course_name', models.CharField(default='Course Name', max_length=30)),
            ],
        ),
        migrations.AlterField(
            model_name='course',
            name='code',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='course_code', to='assignment_info.cname'),
        ),
    ]
