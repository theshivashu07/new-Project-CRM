# Generated by Django 4.0.6 on 2023-01-27 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_Client', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientinfo',
            name='ProfilePick',
            field=models.ImageField(default=None, max_length=75, upload_to='client/'),
        ),
    ]
