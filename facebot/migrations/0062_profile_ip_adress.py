# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-25 16:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebot', '0061_auto_20180324_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='ip_adress',
            field=models.CharField(max_length=255, null=True),
        ),
    ]