# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-11 19:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebot', '0041_oncetask_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='oncetask',
            name='run_date',
            field=models.DateTimeField(null=True),
        ),
    ]
