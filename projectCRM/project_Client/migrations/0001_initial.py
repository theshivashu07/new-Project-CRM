# Generated by Django 4.0.6 on 2023-01-23 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FirstName', models.CharField(max_length=25)),
                ('LastName', models.CharField(max_length=25)),
                ('FullName', models.CharField(max_length=50)),
                ('EmailId', models.CharField(max_length=30)),
                ('MobileNo', models.IntegerField()),
                ('Organization', models.CharField(max_length=30)),
                ('Language', models.CharField(max_length=30)),
                ('Address', models.CharField(max_length=50)),
                ('ZipCode', models.IntegerField()),
                ('State', models.CharField(max_length=25)),
                ('Country', models.CharField(max_length=25)),
                ('JoiningDate', models.DateTimeField(auto_now_add=True)),
                ('ProfilePick', models.ImageField(upload_to='_uploads/client/')),
            ],
        ),
    ]
