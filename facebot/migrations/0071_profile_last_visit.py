# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-25 21:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebot', '0070_auto_20180325_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='last_visit',
            field=models.DateTimeField(null=True),
        ),
    ]