# Generated by Django 4.0.6 on 2023-02-07 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_HR', '0005_alter_employee_profilepick'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='ProfilePick',
            field=models.ImageField(default=None, max_length=75, null=True, upload_to='employee/'),
        ),
    ]
