# Generated by Django 3.2.15 on 2022-10-06 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0019_auto_20221003_2245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='username',
        ),
    ]