# Generated by Django 4.0.6 on 2023-02-20 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_Admin', '0007_allmessages_allsuggestions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allsuggestions',
            name='SenderID',
            field=models.IntegerField(blank=True, default=None),
        ),
    ]
