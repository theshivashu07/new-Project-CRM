# Generated by Django 4.0.6 on 2023-02-19 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_Admin', '0005_alter_reportsormessages_finalsubmission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportsormessages',
            name='FinalSubmission',
        ),
    ]
