# Generated by Django 4.0.6 on 2023-02-28 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_ProjectManager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='alltasks',
            name='TaskStatus',
            field=models.BooleanField(default=False),
        ),
    ]
