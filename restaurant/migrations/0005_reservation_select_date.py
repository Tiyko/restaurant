# Generated by Django 3.2.15 on 2022-09-24 13:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_auto_20220924_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='select_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]