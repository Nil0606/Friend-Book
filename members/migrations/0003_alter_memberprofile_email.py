# Generated by Django 3.2 on 2022-07-06 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_alter_memberprofile_phonenumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberprofile',
            name='email',
            field=models.CharField(max_length=50),
        ),
    ]
